# -*- coding: utf-8 -*-

"""
For interactions with Cloudbreak

Warnings:
    Experimental, not extensively tested
"""

from __future__ import absolute_import
import logging
import base64
import re
import os
from datetime import datetime, timedelta
from calendar import timegm
import json
import six
import nipyapi
from nipyapi.cloudbreak.rest import ApiException
from nipyapi import utils

__all__ = [
    "list_credentials", 'create_credential', 'list_blueprints', 'list_recipes',
    'create_blueprint', 'delete_blueprint', 'get_blueprint', 'create_recipe',
    'delete_recipe', 'list_image_catalogs', 'create_image_catalog',
    'delete_image_catalog', 'get_images', 'get_regions_by_credential',
    'get_custom_params', 'get_credential', 'get_blueprint', 'get_images',
    'list_mpacks', 'create_mpack', 'delete_mpack', 'list_stacks',
    'get_stack_matrix', 'get_default_security_rules', 'get_ssh_keys',
    'prep_placement', 'prep_cluster', 'prep_dependencies', 'purge_cloudbreak',
    'prep_images_dependency', 'prep_stack_specs', 'purge_resource',
    'prep_instance_groups', 'prep_network', 'create_stack', 'delete_stack',
    'delete_credential', 'get_events', 'monitor_event_stream',
]

log = logging.getLogger(__name__)

# Supported Resource Source locations in this code
valid_source_types = ['url', 'file']
# Separator char when parsing readable nested dict keys in this code
sep = ':'


class Horton:
    """
    Borg Singleton to share state between the various processes.
    Looks complicated, but it makes the rest of the code more readable for
    Non-Python natives.
    ...
    Why Horton? Because an Elephant Never Forgets
    """
    __shared_state = {}
    cred = None
    resources = None
    secret = None
    specs = None
    stacks = None
    deps = None

    def __new__(cls, *args, **kwargs):
        """Implements the Borg Singleton Effect"""
        obj = super(Horton, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls.__shared_state
        return obj

    def __init__(self):
        self.cred = None  # Credential for deployments, once loaded in CB
        self.resources = {}  # all loaded resources from github/files
        self.secret = {}  # secrets, keys, passwords and other common controls
        self.defs = []  # definitions of demos, once pulled from resources
        self.specs = {}  # stack specifications, once formulated
        self.stacks = []  # stacks deployed, once submitted
        self.deps = {}  # Dependencies loaded for a given Demo

    def find(self, items):
        """
        Convenience function to retrieve params in a very readable method

        Args:
            items (str): dot notation string of the key for the value to be
                retrieved. e.g 'secret.cloudbreak.hostnme'

        Returns:
            The value if found, or None if not
        """
        return nipyapi.utils.get_val(self, items, sep)


def list_credentials(**kwargs):
    return nipyapi.cloudbreak.V1credentialsApi().get_publics_credential(
        **kwargs
    )


def create_credential(horton=None, platform='AWS', desc='', name=None,
                      params=None, prefix=None, purge=False, **kwargs):
    if horton:
        platform = horton.find('secret:deploycred:platform')
        desc = horton.find('secret:deploycred:desc')
        name = horton.find('secret:deploycred:name')
        params = horton.find('secret:deploycred:params')
        prefix = horton.find('secret:control:namespace')
        global_purge = horton.find('secret:control:purge')
    else:
        global_purge = False

    name = prefix + name if prefix else name  # convenience
    selector = horton.find('secret:deploycred:params:selector')

    if purge or global_purge:
        log.info("Credential Purge set, removing [%s]", name)
        target = [x.id for x in list_credentials() if x.name == name]
        if target:
            delete_credential(target[0])
    log.info("Creating Credential [%s] for platform [%s] with description "
             "[%s]. Params redacted",
             name, platform, desc)

    if platform == 'AWS':
        if selector == 'role-based':
            sub_params = {x:y for x,y in params.items()
                          if x in ['selector', 'roleArn']}
        elif selector == 'key-based':
            sub_params = {x: y for x, y in params.items()
                          if x in ['selector', 'secretKey', 'accessKey']}
        else:
            raise ValueError("selector [%s] unrecognised for platform [%s]",
                             selector, platform)
    else:
        raise ValueError("Platform [%s] unsupported", platform)
    return nipyapi.cloudbreak.V1credentialsApi().post_private_credential(
        body=nipyapi.cloudbreak.CredentialRequest(
            cloud_platform=platform,
            description=desc,
            name=name,
            parameters=sub_params
        ),
        **kwargs
    )


def get_credential(identifier, identifier_type='name', **kwargs):
    return nipyapi.cloudbreak.V1credentialsApi().get_private_credential(
        name=identifier,
        **kwargs
    )


def delete_credential(identifier, identifier_type='id', **kwargs):
    return nipyapi.cloudbreak.V1credentialsApi().delete_credential(
        id=identifier
    )


def list_blueprints(**kwargs):
    return nipyapi.cloudbreak.V1blueprintsApi().get_publics_blueprint(**kwargs)


def create_blueprint(name, desc, blueprint, tags=None, **kwargs):
    log.info("Creating Blueprint [%s] with desc [%s] with Tags [%s]",
             name, desc, str(tags))
    return nipyapi.cloudbreak.V1blueprintsApi().post_private_blueprint(
        body=nipyapi.cloudbreak.BlueprintRequest(
            description=desc,
            name=name,
            ambari_blueprint=base64.b64encode(
                json.dumps(blueprint).encode()
            ).decode(),
            tags=tags
        )
    )


def delete_blueprint(bp_id, **kwargs):
    try:
        return nipyapi.cloudbreak.V1blueprintsApi().delete_blueprint(
            id=bp_id,
            **kwargs
        )
    except ApiException as e:
        raise e


def get_blueprint(identifier, identifier_type='name', **kwargs):
    if identifier_type == 'name':
        bp_info = nipyapi.cloudbreak.V1blueprintsApi().get_public_blueprint(
            name=identifier,
            **kwargs
        )
        bp_content = utils.load(bp_info.ambari_blueprint, decode='base64')
        return bp_info, bp_content
    else:
        raise ValueError("bad identifier type")


def create_recipe(name, desc, recipe_type, recipe, purge=False, **kwargs):
    log.info("Creating recipe [%s] with description [%s] of type [%s] with "
             "recipe like [%s] and purge:[%s]",
             name, desc, recipe_type, json.dumps(recipe)[:50], purge)
    if purge:
        target = [x.id for x in list_recipes() if x.name == name]
        if target:
            delete_recipe(target[0])
    return nipyapi.cloudbreak.V1recipesApi().post_private_recipe(
        # blueprint has to be a base64 encoded string for file upload
        body=nipyapi.cloudbreak.RecipeRequest(
            name=name,
            description=desc,
            recipe_type=recipe_type.upper(),
            content=(
                base64.b64encode(
                    bytes(recipe, 'utf-8')
                )
            ).decode('utf-8')
        ),
        **kwargs
    )


def list_recipes(**kwargs):
    return nipyapi.cloudbreak.V1recipesApi().get_publics_recipe(**kwargs)


def delete_recipe(rp_id, **kwargs):
    try:
        return nipyapi.cloudbreak.V1recipesApi().delete_recipe(
            id=rp_id,
            **kwargs
        )
    except ApiException as e:
        raise e


def list_image_catalogs(**kwargs):
    return nipyapi.cloudbreak.V1imagecatalogsApi().get_publics_image_catalogs(
        **kwargs
    )


def create_image_catalog(name, url, **kwargs):
    log.info("Creating Image Catalog [%s] at url [%s]",
             name, url)
    return nipyapi.cloudbreak.V1imagecatalogsApi().post_private_image_catalog(
        body=nipyapi.cloudbreak.ImageCatalogRequest(
            name=name,
            url=url,
        ),
        **kwargs
    )


def delete_image_catalog(name, **kwargs):
    assert isinstance(name, six.string_types)
    api = nipyapi.cloudbreak.V1imagecatalogsApi()
    return api.delete_public_image_catalog_by_name(
        name=name,
        **kwargs
    )


def get_images(platform, catalog=None, **kwargs):
    if catalog:
        return nipyapi.cloudbreak.V1imagecatalogsApi()\
            .get_public_images_by_provider_and_custom_image_catalog(
            name=catalog,
            platform=platform,
            **kwargs
        )
    return nipyapi.cloudbreak.V1imagecatalogsApi() \
        .get_images_by_provider(
        platform=platform,
        **kwargs
    )


def get_regions_by_credential(cred_name, **kwargs):
    return nipyapi.cloudbreak.V2connectorsApi().get_regions_by_credential_id(
        body=nipyapi.cloudbreak.PlatformResourceRequestJson(
            credential_name=cred_name,
            **kwargs
        )
    )


def get_custom_params(bp_name, **kwargs):
    return nipyapi.cloudbreak.V1utilApi().get_custom_parameters(
        body=nipyapi.cloudbreak.ParametersQueryRequest(
            blueprint_name=bp_name,
        ),
        **kwargs
    )


def list_stacks(**kwargs):
    return nipyapi.cloudbreak.V2stacksApi().get_publics_stack_v2(**kwargs)


def get_stack_matrix(**kwargs):
    return nipyapi.cloudbreak.V1utilApi().get_stack_matrix_util(**kwargs)


def get_default_security_rules(**kwargs):
    return nipyapi.cloudbreak.V1securityrulesApi().get_default_security_rules(
        **kwargs
    )


def get_ssh_keys(params, **kwargs):
    body = nipyapi.cloudbreak.RecommendationRequestJson()
    _ = {body.__setattr__(x, y) for x, y in params.items()}
    return nipyapi.cloudbreak.V1connectorsApi().get_platform_s_sh_keys(
        body=body,
        **kwargs
    )


def list_mpacks(**kwargs):
    return nipyapi.cloudbreak.V1mpacksApi().get_public_management_packs()


def create_mpack(name, desc, url, purge_on_install, **kwargs):
    log.info("Creating MPack [%s] with desc [%s] from url [%s] with "
             "purge_on_install as [%s]",
             name, desc, url[:50], purge_on_install)
    return nipyapi.cloudbreak.V1mpacksApi().post_public_management_pack(
        body=nipyapi.cloudbreak.ManagementPackRequest(
            name=name,
            description=desc,
            mpack_url=url,
            purge=purge_on_install
        )
    )


def delete_mpack(name, **kwargs):
    assert isinstance(name, six.string_types)
    return nipyapi.cloudbreak.V1mpacksApi().delete_public_management_pack(
        name=name
    )


def prep_dependencies(horton=None, demos=None, resources=None, prefix=None,
                      purge=False):
    if not horton:
        horton.defs = demos
        horton.resources = resources
        horton.secret['control']['namespace'] = prefix
        horton.secret['control']['purge'] = purge
    else:
        purge = horton.find('secret:control:purge')  # convenience
        prefix = horton.secret['control']['namespace']  # convenience

    supported_resouces = ['recipe', 'blueprint', 'catalog', 'mpack']
    current = {
        'blueprint': list_blueprints(),
        'recipe': list_recipes(),
        'catalog': list_image_catalogs(),
        'mpack': list_mpacks()
    }

    for demo in horton.defs:
        demo_name = demo['name']
        deps = {}
        log.info("---- Checking Dependencies for Demo [%s]", demo_name)
        log.debug("Demo like [%s]", json.dumps(demo))
        for res_type in [x for x in demo.keys() if x in supported_resouces]:
            log.debug("res_type like [%s]", res_type)
            res_defs = demo[res_type]
            if not isinstance(res_defs, list):
                res_defs = [res_defs]
            for res in res_defs:
                log.debug("resource like [%s]", json.dumps(res))
                dep = None
                if not res:
                    # resource in def, but not populated
                    log.info("Resource for res_type [%s] not in demo [%s], "
                             "skipping...", res_type, demo['name'])
                    break
                log.info("checking Resource type [%s]", res_type)
                if 'name' in res and res['name']:
                    res_name = prefix + res['name'] if prefix else res['name']
                    log.info("Resource has default Name [%s], namespace is "
                             "[%s], so using Name [%s]",
                             res['name'], prefix, res_name)
                else:
                    # res has name field but not populated
                    log.info("Resource name field present but empty, "
                             "skipping...")
                    break
                if not horton.find('secret:control:purge'):
                    if 'purge' in res:
                        purge = res['purge']
                        # If not global purge, use resource specific setting
                if not purge:
                    # if not purging resource, check it's not already loaded
                    dep = [x for x in current[res_type] if res_name == x.name]
                    if dep:
                        log.info("Resource [%s]:[%s] already loaded and Purge "
                                 "not set, skipping...",
                                 res_type, res_name)
                else:
                    purge_resource(res_name, res_type)
                desc = res['desc'] if 'desc' in res else ''
                if res_type not in deps and res_type in ['recipe', 'mpack']:
                    # Treat everything as a list for simplicity
                    deps[res_type] = []
                if res_type == 'blueprint':
                    if dep:
                        deps[res_type] = dep[0]
                    else:
                        deps[res_type] = \
                            nipyapi.deploy.create_blueprint(
                                source='file',
                                desc=desc,
                                name=res_name,
                                blueprint=horton.find(
                                    'resources:' + res['def'].replace(os.sep,
                                                                      sep)
                                )
                            )
                if res_type == 'catalog':
                    if dep:
                        deps[res_type] = dep[0]
                    else:
                        deps[res_type] = \
                            nipyapi.deploy.create_image_catalog(
                            name=res_name,
                            url=demo[res_type]['def']
                        )

                if res_type == 'recipe':
                    if dep:
                        deps[res_type].append(dep[0])
                    else:
                        deps[res_type].append(
                            nipyapi.deploy.create_recipe(
                                name=res_name,
                                desc=desc,
                                recipe_type=res['typ'],
                                recipe=horton.find(
                                    'resources:' + res['def'].replace(
                                        os.sep, sep
                                    )
                                )
                            )
                        )
                if res_type == 'mpack':
                    if dep:
                        deps[res_type].append(dep[0])
                    else:
                        if 'purge_on_install' in res:
                            purge_on_install = res['purge_on_install']
                        else:
                            purge_on_install = False
                        deps[res_type].append(
                            create_mpack(
                                name=res_name,
                                desc=desc,
                                url=res['url'],
                                purge_on_install=purge_on_install
                            )
                        )
        horton.deps[demo_name] = deps
        prep_images_dependency(demo_def=demo, horton=horton)
        horton.deps[demo_name]['gateway'] = find_ambari_group(
            demo_def=demo, horton=horton
        )

    if not horton:
        return horton.deps


def find_ambari_group(demo_def, horton):
    # Find Ambari Group
    demo_key = demo_def['name']
    # If only one group, it must be the gateway
    if 'group' in demo_def:
        if len(demo_def['group']) == 1:
            return demo_def['group'][0]['name']
        else:
            test =[x['name'] for x in demo_def['group'] if x['type'] == 'GATEWAY']
            if test:
                # If the demo has a gateway defined, use it
                return test[0]
            else:
                # Else raise an error for bad group config
                raise ValueError("No GATEWAY specified in Group config")
    else:
        # Try finding it in the Blueprint
        bp_content = utils.load(
            horton.deps[demo_key]['blueprint'].ambari_blueprint,
            decode='base64'
        )
        for host_group in bp_content['host_groups']:
            for component in host_group['components']:
                if component['name'] == 'AMBARI_SERVER':
                    return host_group['name']
    raise ValueError("Couldn't find Gateway or Ambari Server in definitions")


def prep_placement(cred, placement_def):
    log.info("prepping stack placement settings")
    log.info("fetching region info for credential [%s]", cred.name)
    region_info = get_regions_by_credential(cred.name)
    if placement_def['region'] is None:
        t_region = region_info.default_region
    else:
        t_region = [
            x for x in region_info.regions if x == placement_def['region']
        ]
    if not t_region:
        raise ValueError("Region [%s] not available for credential [%s]",
                         placement_def['region'], cred.name)
    if placement_def['avzone']:
        t_av_zone = [
            x for x in region_info.availability_zones[t_region]
            if x == placement_def['avzone']
        ]
    else:
        t_av_zone = region_info.availability_zones[t_region][0]
    if not t_av_zone:
        raise ValueError("Availability Zone [%s] not available for credential "
                         "[%s]", t_av_zone, cred.name)
    log.info("location definition contained region:availabilty zone [%s]:[%s],"
             " returning config with [%s]:[%s]",
             str(placement_def['region']), str(placement_def['avzone']),
             t_region, t_av_zone)
    return nipyapi.cloudbreak.PlacementSettings(
                region=t_region,
                availability_zone=t_av_zone
            )


def prep_images_dependency(demo_def, horton):
    log.info("Prepping valid images for demo spec")
    cat_name = demo_def['catalog']['name'] if 'name' in demo_def['catalog'] else None
    demo_key = demo_def['name']
    tgt_os = demo_def['infra']['os']
    bp_content = utils.load(
        horton.deps[demo_key]['blueprint'].ambari_blueprint, decode='base64'
    )
    stack_name = bp_content['Blueprints']['stack_name']
    stack_version = bp_content['Blueprints']['stack_version']
    log.info("fetching stack matrix for name:version [%s]:[%s]",
             stack_name, stack_version)
    stack_matrix = nipyapi.deploy.get_stack_matrix()
    stack_root = nipyapi.utils.get_val(
        stack_matrix,
        [stack_name.lower(),
         bp_content['Blueprints']['stack_version']]
    )
    images = nipyapi.deploy.get_images(
        catalog=cat_name,
        platform=horton.cred.cloud_platform
    )
    log.info("Fetched images from Cloudbreak [%s]", str(images.attribute_map)[:100])

    images_by_os = [
        x for x in
        images.base_images + images.__getattribute__(stack_name.lower() + '_images')
    ]
    if tgt_os:
        _ = [x for x in images_by_os if x.os == tgt_os]
    log.info("Filtered images by OS [%s] and found [%d]", tgt_os,
             len(images_by_os))
    valid_images = []
    for image in images_by_os:
        if type(image) == nipyapi.cloudbreak.BaseImageResponse:
            ver_check = [
                x.version for x in image.__getattribute__(
                    '_'.join([stack_name.lower(), 'stacks'])
                ) if x.version == stack_root.version
            ]
            if ver_check:
                valid_images.append(image)
        elif type(image) == nipyapi.cloudbreak.ImageResponse:
            if image.stack_details.version == stack_root.version:
                valid_images.append(image)

    if valid_images:
        log.info("found [%d] images matching requirements", len(valid_images))
        horton.deps[demo_key]['images'] = valid_images
    else:
        raise ValueError("No Valid Images found for stack definition")


def prep_cluster(demo_def, horton):
    log.info("prepping stack cluster settings")
    if not horton:
        raise ValueError("This convenience function doesn't support "
                         "individual params")
    demo_key = demo_def['name']
    tgt_os_name = horton.deps[demo_key]['images'][0].os
    prefix = horton.secret['control']['namespace']  # convenience
    mpacks = [{'name': x['name']}
              for x in demo_def['mpack']
              ] if demo_def['mpack'] else []
    if prefix:
        mpacks = [{'name': prefix + x['name']} for x in mpacks]
    bp_content = utils.load(
        horton.deps[demo_key]['blueprint'].ambari_blueprint, decode='base64'
    )
    stack_name = bp_content['Blueprints']['stack_name']
    stack_version = bp_content['Blueprints']['stack_version']

    # Cloud Storage
    object_store = horton.find('secret:cloudstor:objectstore')
    if object_store:
        if object_store == 's3':
            bucket = horton.find('secret:cloudstor:bucket')
            cloud_stor = nipyapi.cloudbreak.CloudStorageRequest(
                s3=nipyapi.cloudbreak.S3CloudStorageParameters(
                    instance_profile=horton.find('secret:cloudstor:role')
                ),
                locations=[]
            )
            if demo_def['infra']['cloudstor']:
                for loc in demo_def['infra']['cloudstor']:
                    cloud_stor.locations.append({
                        "value": "s3a://" + bucket + loc['value'],
                        "propertyFile": loc['propfile'],
                        "propertyName": loc['propname']
                    })
        else:
            raise ValueError("Object Store [%s] not supported", object_store)
    else:
        cloud_stor = None

    log.info("using mpack [%s]", str(mpacks))

    cluster_req = nipyapi.cloudbreak.ClusterV2Request(
                ambari=nipyapi.cloudbreak.AmbariV2Request(
                    blueprint_name=horton.deps[demo_key]['blueprint'].name,
                    ambari_stack_details=nipyapi.cloudbreak.AmbariStackDetails(
                        version=stack_version,
                        verify=False,
                        enable_gpl_repo=False,
                        stack=stack_name,
                        os=tgt_os_name,
                        mpacks=mpacks
                    ),
                    user_name=horton.find('secret:clustercred:username'),
                    password=horton.find('secret:clustercred:password'),
                    validate_blueprint=False,  # Hardcoded?
                    ambari_security_master_key=horton.find(
                        'secret:clustercred:masterkey'),
                    enable_security=False  # Hardcoded?
                ),
                cloud_storage=cloud_stor
            )
    if 'stackrepo' in demo_def['infra']:
        cluster_req.ambari.ambari_stack_details.repository_version = demo_def['infra']['stackrepo']['ver']
        cluster_req.ambari.ambari_stack_details.version_definition_file_url = demo_def['infra']['stackrepo']['url']
    if 'ambarirepo' in demo_def['infra']:
        ambari_repo = {
            x: y for x, y in demo_def['infra']['ambarirepo'].items()
        }
        cluster_req.ambari.ambari_repo_details_json = ambari_repo
    return cluster_req


def prep_instance_groups(demo_def, horton=None):
    log.info("Prepping instance groups")
    if not horton:
        raise ValueError("This convenience function doesn't support "
                         "individual params")
    prefix = horton.find('secret:control:namespace')
    demo_key = demo_def['name']
    region = horton.specs[demo_key].placement.region
    avzone = horton.specs[demo_key].placement.availability_zone
    log.info("Fetching Infrastructure recommendation for "
             "credential[%s]:blueprint[%s]:region[%s]:availability zone[%s]",
             horton.cred.name, horton.deps[demo_key]['blueprint'].name,
             region, avzone)

    recs = nipyapi.cloudbreak.V1connectorsApi().create_recommendation(
        body=nipyapi.cloudbreak.RecommendationRequestJson(
            availability_zone=avzone,
            region=region,
            blueprint_id=horton.deps[demo_key]['blueprint'].id,
            credential_id=horton.cred.id
        )
    )
    log.info("Handling Security Rules")
    sec_group = horton.find('secret:infra:securityGroupId')
    if sec_group:
        # Predefined Security Group
        sec_group = nipyapi.cloudbreak.SecurityGroupResponse(
            security_group_id=sec_group,
            cloud_platform=horton.find('secret:deploycred:platform')
        )
    else:
        raise ValueError("Network Security Group not Provided")
    groups = []
    log.info("found recommendations for instance groups [%s]",
             str(recs.recommendations.keys()))
    for group in recs.recommendations.keys():
        log.info("handling group [%s]", group)
        rec = recs.recommendations[group]
        group_def = [x for x in demo_def['group'] if x['name'] == group]
        if group_def:
            group_def = group_def[0]
            log.info("Group [%s] found in demo def, proceeding...",
                     group)
        else:
            log.info("Group [%s] not in demo def, using defaults...", group)
            group_def = {}
        nodes = group_def['nodes'] if 'nodes' in group_def else 1
        machine = group_def['machine'] if 'machine' in group_def else None
        if prefix:
            if 'recipe' in group_def and group_def['recipe'] is not None:
                recipes = [prefix + x for x in group_def['recipe']]
            else:
                recipes = []
        else:
            recipes = group_def['recipe'] if 'recipe' in group_def else []
        log.info("Using Recipe list [%s]", str(recipes))
        if horton.deps[demo_key]['gateway'] == group:
            # This is the Ambari group
            typ = 'GATEWAY'
        else:
            typ = 'CORE'
        disk_types = [x.name for x in recs.disk_responses]
        vol_type = sorted([
            x for x in disk_types
            if x in demo_def['infra']['disktypes']])[0]
        log.info("selected disk type [%s] from preferred list [%s] out of "
                 "available types [%s]",
                 vol_type, str(demo_def['infra']['disktypes']),
                 str(disk_types))
        root_vol_size = rec.vm_type_meta_json.properties[
                            'recommendedRootVolumeSize']
        log.info("using root vol size [%s]", root_vol_size)
        vol_count = rec.vm_type_meta_json.properties[
                            'recommendedvolumeCount']
        vol_size = rec.vm_type_meta_json.properties[
                            'recommendedvolumeSizeGB']
        log.info("using [%s] volumes of size [%s]", vol_count, vol_size)
        item = nipyapi.cloudbreak.InstanceGroupsV2(
                    security_group=sec_group,
                    template=nipyapi.cloudbreak.TemplateV2Request(
                        parameters={
                            'encrypted': False  # Hardcoded?
                        },
                        instance_type=machine if machine else rec.value,
                        volume_count=vol_count,
                        volume_size=vol_size,
                        root_volume_size=root_vol_size,
                        volume_type=vol_type
                    ),
                    node_count=nodes,
                    group=group,
                    type=typ,
                    recovery_mode='MANUAL',  # Hardcoded?
                    recipe_names=recipes
            )
        groups.append(item)
    log.info("Finished Prepping Groups")
    return groups


def prep_network(infra_def, horton):
    log.info("preparing network configuration")
    if infra_def['subnet']:
        subnet = infra_def['subnet']
        params = {}
    else:
        subnet = None
        params = {x: y for x, y in horton.find('secret:infra').items()
                  if x in ['vpcId', 'subnetId']}
    log.info("found subnet [%s] in infra definition, using [%s]",
             str(infra_def['subnet']), subnet)
    log.info("using additional network parameters of [%s]", str(params))
    return nipyapi.cloudbreak.NetworkV2Request(
                parameters=params,
                subnet_cidr=subnet
            )


def prep_stack_specs(horton=None, demos=None, deps=None, cred=None,
                     secret=None, prefix=None):
    if not horton:
        horton.defs = demos
        horton.cred = cred
        horton.deps = deps
        horton.secret = secret
        horton.secret['control']['namespace'] = prefix
    else:
        prefix = horton.find('secret:control:namespace')  # convenience

    for demo_def in horton.defs:
        demo_key = demo_def['name']
        cat_name = demo_def['catalog']['name'] if demo_def['catalog'][
            'name'] else None
        log.info("preparing spec for demo [%s]", demo_key)
        cluster_name = prefix + demo_key if prefix else demo_key

        # Sequence matters here, as some later params are have deps in earlier
        # Which also means you can't be clever and define it in one big call
        # Making Placeholder
        horton.specs[demo_key] = nipyapi.cloudbreak.StackV2Request(
            general='', instance_groups=''
        )
        # Populating
        horton.specs[demo_key].tags = {
            'Owner': horton.cred.name,
            'EndDate': (
                datetime.now() + timedelta(days=2)).strftime("%d%b%Y"),
            'StartDate': datetime.now().strftime("%d%b%Y")
        }
        horton.specs[demo_key].network = prep_network(
            infra_def=demo_def['infra'],
            horton=horton
        )
        horton.specs[demo_key].stack_authentication = \
            nipyapi.cloudbreak.StackAuthenticationResponse(
                    public_key_id=horton.find('secret:infra:sshkey')
                )
        horton.specs[demo_key].general = nipyapi.cloudbreak.GeneralSettings(
                credential_name=horton.cred.name,
                name=cluster_name
            )
        horton.specs[demo_key].image_settings = \
            nipyapi.cloudbreak.ImageSettings(
                image_catalog=cat_name,
                image_id=horton.deps[demo_key]['images'][0].uuid
            )
        horton.specs[demo_key].placement = prep_placement(
                cred=horton.cred,
                placement_def=demo_def['placement']
            )
        horton.specs[demo_key].cluster = prep_cluster(
                    demo_def=demo_def,
                    horton=horton
                )
        if 'input' in demo_def:
            horton.specs[demo_key].inputs = demo_def['input']
        horton.specs[demo_key].instance_groups = prep_instance_groups(
                demo_def=demo_def,
                horton=horton
            )
    if not horton:
        return horton.specs


def create_stack(spec, wait=False, **kwargs):
    start_ts = datetime.utcnow()
    resp = nipyapi.cloudbreak.V2stacksApi().post_private_stack_v2(
        body=spec,
        **kwargs
    )
    if wait:
        nipyapi.utils.wait_to_complete(
            monitor_event_stream,
            start_ts=start_ts,
            identity=('stack_id', resp.id),
            target_event=('stack_status', 'AVAILABLE'),
            valid_events=[
                'UPDATE_IN_PROGRESS', 'BILLING_STARTED', 'AVAILABLE',
                'CREATE_IN_PROGRESS'
            ],
            nipyapi_delay=15,
            nipyapi_max_wait=wait
        )
    return resp


def delete_stack(stack_id, force=False, wait=True, **kwargs):
    log.info("Requesting delete of Stack [%d] params Force [%s] and Wait "
             "[%s]", stack_id, force, wait)
    start_ts = datetime.utcnow()
    resp = nipyapi.cloudbreak.V2stacksApi().delete_stack_v2(
        id=stack_id,
        forced=force,
        **kwargs
    )
    if wait:
        nipyapi.utils.wait_to_complete(
            monitor_event_stream,
            start_ts=start_ts,
            identity=('stack_id', stack_id),
            target_event=('stack_status', 'DELETE_COMPLETED'),
            valid_events=['DELETE_IN_PROGRESS'],
            nipyapi_delay=20,
            nipyapi_max_wait=300
        )
    return resp


def monitor_event_stream(start_ts, identity, target_event, valid_events,
                         **kwargs):
    log.info("Monitoring event stream from [%s] for Event [%s] for Identity "
             "[%s] against Valid Events [%s]",
             str(start_ts), str(target_event), str(identity), str(valid_events))
    events = nipyapi.deploy.get_events(
        start_ts=start_ts,
        select_by=identity,
    )
    event_set = set([x.__getattribute__(target_event[0])
                     for x in events])
    log.info("Found event set [%s] for target event [%s]",
             str(event_set), target_event[0])
    if target_event[1] in event_set:
        return True
    valid_test = [x for x in event_set if x not in valid_events]
    if valid_test:
        raise ValueError("Found Event {0} for Identity {1} which is not in"
                         "Valid Event list {2}".format(
            str(valid_test), str(identity), str(valid_events)))
    return False


def get_events(start_ts=None, select_by=None, ordered_by='event_timestamp',
               raw_input=False, raw_output=False):
    # ts from Cloudbreak are natively in ms, which breaks some python calls
    if start_ts:
        # raw_input means pas the start_ts unhindered
        # otherwise it's treated as a python datetime object
        if raw_input:
            submit_ts = start_ts
        else:
            # standard pythong ts is in s, so x1000 for ms
            # as Cloudbreak seems to assume that all ts are in ms
            submit_ts = timegm(start_ts.timetuple()) * 1000
        events = nipyapi.cloudbreak.V1eventsApi().get_events(
            since=submit_ts)
    else:
        events = nipyapi.cloudbreak.V1eventsApi().get_events()
    # Handle filtering whole events by a particular (field, key) tuple
    if not select_by:
        selected = events
    else:
        selected = [
            x for x in events
            if x.__getattribute__(select_by[0]) == select_by[1]
        ]
    # convert ts to s in datetime if requested, should be this by default
    if not raw_output:
        for e in selected:
            _ = {e.__setattr__(
                k,
                datetime(1970, 1, 1) + timedelta(milliseconds=e.event_timestamp)
            )
             for k in e.swagger_types.keys()
             if k == 'event_timestamp'}
    # return list of events sorted by ordered_by, defaults to event time
    return sorted(selected, key=lambda k: k.__getattribute__(ordered_by))


def purge_resource(res_name, res_type):
    log.info("Requested to Purge Resource [%s] of Type [%s]",
             res_name, res_type)
    # check for compatibility
    res_types = ['recipe', 'mpack', 'stack', 'blueprint', 'credential',
                 'recipe', 'catalog']
    if res_type in res_types:
        # Set the param to identify the target resource

        if res_type in ['catalog', 'mpack']:
            del_arg = 'name'
        else:
            del_arg = 'id'
        # rename if necessary

        if res_type == 'catalog':
            res_type = 'image_catalog'

        # set extra kwargs for submission
        if res_type == 'stack':
            params = {
                'force': True,
                'wait': True
            }
        else:
            params = {}
    else:
        raise ValueError("res_type [%s] unsupported", res_type)
    # select functions
    target = [x for x in getattr(nipyapi.deploy, 'list_' + res_type + 's')()
              if x.name == res_name]
    if not target:
        log.info("Resource named [%s] of Type [%s] not found, skipping delete",
                 res_name, res_type)
        return
    try:
        log.info("Attempting Delete of [%s]:[%s] identified by [%s]",
                 res_type, res_name, del_arg)
        getattr(nipyapi.deploy, 'delete_' + res_type)(
            target[0].__getattribute__(del_arg),
            **params
        )
        log.info("Deleted [%s]:[%s] identified by [%s]",
                 res_type, res_name, del_arg)
    except ApiException as e:
        if 'Please remove this cluster' in e.body:
            log.info("Delete blocked by dependency, requesting Purge of "
                     "dependency")
            new_target = re.search('cluster \[\'(.*?)\'\]', e.body)
            purge_resource(
                res_type='stack',
                res_name=new_target.group(1)
            )
            # Try again, still recursively
            purge_resource(
                res_type=res_type,
                res_name=res_name
            )
        else:
            raise e
    # execute


def purge_cloudbreak(for_reals, namespace=''):
    if not for_reals:
        raise ValueError("Cowardly not purging Cloudbreak as you didn't say "
                         "for reals. Please check function definition")
    # Stacks first because of dependencies
    log.info("Purging stacks")
    [delete_stack(x.id, force=True)
     for x in list_stacks()
     if namespace in x.name]
    # Then other stuff
    # Images
    log.info("Purging Images")
    [delete_image_catalog(x.name)
     for x in list_image_catalogs()
     if x.used_as_default is False and namespace in x.name]
    # Blueprints
    log.info("Purging Blueprints")
    [delete_blueprint(x.id)
     for x in list_blueprints()
     if namespace in x.name]
    # Recipes
    log.info("Purging Recipes")
    [delete_recipe(x.id)
     for x in list_recipes()
     if namespace in x.name]
    # Credentials
    log.info("Purging Credentials")
    [delete_credential(x.id)
     for x in list_credentials()
     if namespace in x.name]
    # Mpacks
    log.info("Purging MPacks")
    [delete_mpack(x.name)
     for x in list_mpacks()
     if namespace in x.name]
