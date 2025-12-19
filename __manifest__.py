{
    'name': 'Multi-Currency Revaluation (MXN/USD)',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Revaluate foreign currency accounts for MXN legislation',
    'description': """
        Módulo para la revaluación de moneda extranjera (USD a MXN).
        Permite configurar cuentas de provisión y generar asientos de ajuste de cierre.
    """,
    'author': 'Alphaqueb Consulting',
    'depends': ['account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/account_account_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/account_revaluation_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
