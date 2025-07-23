
ROLE_PERMISSIONS = {
    "admin": [
        "create_user",
        "update_user",
        "delete_user",
        "view_all_users",
        "create_loan",
        "approve_loan",
        "reject_loan",
        "view_all_loans",
        "update_repayment_status",
        "view_all_repayments",
        "view_all_clients",
        "generate_report",
        "view_collection_dashboard",
        "view_system_setings",
        "update_system_settings",
        "manage_collections",
        "view_reports",
        "assign_roles",
        "assign_collector_to_clients",
        "export_data",
        "send_notifications",
        "view_all_notifications",
        "view_all_settings",
        "update_settings",
        "view_all_roles",
        "update_roles",
        "view_all_users",

    ],
    "collector": [
        "create_loan",
        "manage_collections",
        "view_reports",
        "view_assgned_clients"
        "view_clients",
        "update_repayment_status",
        "make_repayment",
        "send_notifications",
  
    ],
    "client": [
        "create_loan",
        "view_own_data",
        "view_own_loans"
        "make_repayment",
        "view_own_reports",
        "view_own_repayments",
        "view_own_notifications",
        "update_own_profile",
        "send_notifications",
      
    ],
}