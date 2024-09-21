Leak_Function = [   
    {
        "name": "dehashed-search",
        "description": "Use this for investigating persons or entities. Can handle multiple queries.",
        "parameters": {
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "nickname": {
                                "type": "string",
                                "description": "The nickname to search",
                            },
                            "mail": {
                                "type": "string",
                                "description": "The mail/domain to search, if not full mail is provided, take the domain",
                            },
                        },
                        "required": ["mail", "nickname"],
                    },
                },
            },
            "required": ["queries"],
        },
    },
]