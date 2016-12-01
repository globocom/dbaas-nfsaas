UPDATE dbaas_nfsaas_hostattr
     JOIN physical_host ON (physical_host.id = dbaas_nfsaas_hostattr.host_id)
     JOIN physical_instance ON (physical_instance.hostname_id = physical_host.id)
     JOIN physical_databaseinfra ON (physical_databaseinfra.id = physical_instance.databaseinfra_id)
     JOIN physical_plan ON (physical_plan.id = physical_databaseinfra.plan_id)
     JOIN dbaas_credentials_credential_environments ON (dbaas_credentials_credential_environments.environment_id = physical_databaseinfra.environment_id)
     JOIN dbaas_credentials_credential ON (dbaas_credentials_credential.id = dbaas_credentials_credential_environments.credential_id)
     JOIN dbaas_nfsaas_environmentattr ON (dbaas_nfsaas_environmentattr.dbaas_environment_id = physical_databaseinfra.environment_id)
     JOIN dbaas_nfsaas_planattr ON (dbaas_nfsaas_planattr.dbaas_plan_id = physical_databaseinfra.plan_id)
 SET dbaas_nfsaas_hostattr.nfsaas_team_id = trim(substr(dbaas_credentials_credential.team, 1, 10)),
     dbaas_nfsaas_hostattr.nfsaas_project_id = trim(substr(dbaas_credentials_credential.project, 1, 10)),
     dbaas_nfsaas_hostattr.nfsaas_environment_id = dbaas_nfsaas_environmentattr.nfsaas_environment,
     dbaas_nfsaas_hostattr.nfsaas_size_id = dbaas_nfsaas_planattr.nfsaas_plan
 WHERE physical_instance.instance_type IN (1, 2, 4)
     and physical_plan.provider = 1
     and dbaas_credentials_credential.integration_type_id = 2;
