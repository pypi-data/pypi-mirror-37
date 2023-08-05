from const import ReportTypeMap
groups = {
    'pboc': {
        'query_types': ['async'],
        'report_type': ReportTypeMap.PBOC_MAPING.value,
        'front_args': [
            {'name': 'name', 'type': 'str', 'desc': '姓名'},
            {'name': 'product', 'type': 'str', 'desc': '产品'},
            {'name': 'cert_no', 'type': 'str', 'desc': '证件号'},
            {'name': 'cert_type', 'type': 'str', 'desc': '证件类型'},
            {'name': 'query_reason', 'type': 'str', 'desc': '查询原因'},
            {'name': 'query_type', 'type': 'str', 'desc': '查询类型'}
        ]
    },
    'tongdun': {
        'query_types': ['sync', 'async'],
        'front_args': [
            {'name': 'account_mobile', 'type': 'str', 'desc': '手机号'},
            {'name': 'account_name', 'type': 'str', 'desc': '姓名'},
            {'name': 'id_number', 'type': 'str', 'desc': '证件号'},
            {'name': 'id_type', 'type': 'str', 'desc': '证件类型'}
        ],
        'report_type': ReportTypeMap.TONGDUN_MAPING.value
    },
    'tongdun_anti_fraud': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'account_mobile', 'type': 'str', 'desc': '手机号'},
             {'name': 'account_name', 'type': 'str', 'desc': '姓名'},
             {'name': 'id_number', 'type': 'str', 'desc': '证件号'},
             {'name': 'id_type', 'type': 'str', 'desc': '证件类型'}
        ],
        'report_type': ReportTypeMap.TONGDUN_ANTI_FRAUD_MAPING.value
    },
    'moxie': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'task_id', 'type': 'str', 'desc': '任务id'},
             {'name': 'user_id', 'type': 'str', 'desc': '用户id'},
             {'name': 'product_code', 'type': 'str', 'desc': '产品编码'},
             {'name': 'mobile', 'type': 'str', 'desc': '手机号'}
        ],
        'report_type': ReportTypeMap.MOXIE_MAPING.value
    },
    'shuzun_cur_state': {
         'query_types': ['sync', 'async'],
         'front_args': [
              {'name': 'mobile', 'type': 'str', 'desc': '手机号'},
              {'name': 'product_code', 'type': 'str', 'desc': '产品编码'},
         ],
         'report_type': ReportTypeMap.SHUZUN_CUR_STATE_MAPING.value
    },
    'shuzun_time': {
         'query_types': ['sync', 'async'],
         'front_args': [
              {'name': 'mobile', 'type': 'str', 'desc': '手机号'},
              {'name': 'product_code', 'type': 'str', 'desc': '产品编码'},
         ],
         'report_type': ReportTypeMap.SHUZUN_TIME_MAPING.value
    },
    'shuzun_verification': {
         'query_types': ['sync', 'async'],
         'front_args': [
              {'name': 'mobile', 'type': 'str', 'desc': '手机号'},
              {'name': 'product_code', 'type': 'str', 'desc': '产品编码'},
              {'name': 'id_no', 'type': 'str', 'desc': '身份证号'},
              {'name': 'real_name', 'type': 'str', 'desc': '真实姓名'}
         ],
         'report_type': ReportTypeMap.SHUZUN_VERIFICATION_MAPING.value
    },
    'gongan': {
         'query_types': ['sync', 'async'],
         'front_args': [
              {'name': 'id_no', 'type': 'str', 'desc': '证件号'},
              {'name': 'real_name', 'type': 'str', 'desc': '真实姓名'},
              {'name': 'id_type', 'type': 'str', 'desc': '证件类型'}
         ],
         'report_type': ReportTypeMap.GONGAN_MAPING.value
    },
    'app_type': {
        'query_types': ['async', 'sync'],
        'front_args': [
             {'name': 'app_list', 'type': 'list', 'desc': 'app名称列表'}
        ],
        'report_type': None
    },
    'certno_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'certno', 'type': 'str', 'desc': '证件号'}
        ],
        'report_type': None
    },
    'address_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'address', 'type': 'str', 'desc': '地址'}
        ],
        'report_type': None
    },
    'mobile_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name':  'mobile', 'type': 'str', 'desc': '手机号'}
        ],
        'report_type': None
    },
    'lbs_address_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'lbs_address', 'type': 'str', 'desc': '区域地址'}
        ],
        'report_type': None
    },
    'contact_address_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'contact_address', 'type': 'str', 'desc': '联系地址'}
        ],
        'report_type': None
    },
    'ip_district': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'ip', 'type': 'str', 'desc': 'ip地址'}
        ],
        'report_type': None
    },
    'mobile': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'brand_key', 'type': 'str', 'desc': '手机品牌'},
             {'name': 'model_key', 'type': 'str', 'desc': '手机型号'}
        ],
        'report_type': None
    },
    'certno_record_list': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'certno', 'type': 'str', 'desc': '证件号'}
        ],
        'report_type': None
    },
    'mobile_record_list': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'mobile', 'type': 'str', 'desc': '手机号'}
        ],
        'report_type': None
    },
    'sensitive_contact': {
        'query_types': ['sync', 'async'],
        'front_args': [
             {'name': 'contacts', 'type': 'list', 'desc': '常用联系人列表'}
        ],
        'report_type': None
    }
}
