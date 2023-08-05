function GetOciTopLevelCommand_dns() {
    return 'dns'
}

function GetOciSubcommands_dns() {
    $ociSubcommands = @{
        'dns' = 'record zone'
        'dns record' = 'domain rrset zone'
        'dns record domain' = 'delete get patch update'
        'dns record rrset' = 'delete get patch update'
        'dns record zone' = 'get patch update'
        'dns zone' = 'create delete get list update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_dns() {
    $ociCommandsToLongParams = @{
        'dns record domain delete' = 'compartment-id domain force from-json help if-match if-unmodified-since zone-name-or-id'
        'dns record domain get' = 'all compartment-id domain from-json help if-modified-since if-none-match limit page page-size rtype sort-by sort-order zone-name-or-id zone-version'
        'dns record domain patch' = 'compartment-id domain from-json help if-match if-unmodified-since items zone-name-or-id'
        'dns record domain update' = 'compartment-id domain force from-json help if-match if-unmodified-since items zone-name-or-id'
        'dns record rrset delete' = 'compartment-id domain force from-json help if-match if-unmodified-since rtype zone-name-or-id'
        'dns record rrset get' = 'all compartment-id domain from-json help if-modified-since if-none-match limit page page-size rtype zone-name-or-id zone-version'
        'dns record rrset patch' = 'compartment-id domain from-json help if-match if-unmodified-since items rtype zone-name-or-id'
        'dns record rrset update' = 'compartment-id domain force from-json help if-match if-unmodified-since items rtype zone-name-or-id'
        'dns record zone get' = 'all compartment-id domain domain-contains from-json help if-modified-since if-none-match limit page page-size rtype sort-by sort-order zone-name-or-id zone-version'
        'dns record zone patch' = 'compartment-id from-json help if-match if-unmodified-since items zone-name-or-id'
        'dns record zone update' = 'compartment-id force from-json help if-match if-unmodified-since items zone-name-or-id'
        'dns zone create' = 'compartment-id external-masters from-json help max-wait-seconds name wait-for-state wait-interval-seconds zone-type'
        'dns zone delete' = 'compartment-id force from-json help if-match if-unmodified-since max-wait-seconds wait-for-state wait-interval-seconds zone-name-or-id'
        'dns zone get' = 'compartment-id from-json help if-modified-since if-none-match zone-name-or-id'
        'dns zone list' = 'all compartment-id from-json help lifecycle-state limit name name-contains page page-size sort-by sort-order time-created-greater-than-or-equal-to time-created-less-than zone-type'
        'dns zone update' = 'compartment-id external-masters force from-json help if-match if-unmodified-since max-wait-seconds wait-for-state wait-interval-seconds zone-name-or-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_dns() {
    $ociCommandsToShortParams = @{
        'dns record domain delete' = '? c h'
        'dns record domain get' = '? c h'
        'dns record domain patch' = '? c h'
        'dns record domain update' = '? c h'
        'dns record rrset delete' = '? c h'
        'dns record rrset get' = '? c h'
        'dns record rrset patch' = '? c h'
        'dns record rrset update' = '? c h'
        'dns record zone get' = '? c h'
        'dns record zone patch' = '? c h'
        'dns record zone update' = '? c h'
        'dns zone create' = '? c h'
        'dns zone delete' = '? c h'
        'dns zone get' = '? c h'
        'dns zone list' = '? c h'
        'dns zone update' = '? c h'
    }
    return $ociCommandsToShortParams
}