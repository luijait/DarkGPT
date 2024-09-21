Leak_Function = [   {
        "name": "dehashed-search",
        "description": "You will use this whenever the query is related to any type of action related to the investigation of persons or entities of any kind.",
        "parameters": {
            "type": "object",
            "properties": {
                "nickname": {
                    "type": "string",
                    "description": "The nickname to search",
                },
                "mail": {
                    "type": "string",
                    "description": "The mail/domain to search, if not full mail is provided, take the domain, Please this field should never be the nickname",
                },
      
            },
            "required": ["mail", "nickname"], 
        },

    },
]