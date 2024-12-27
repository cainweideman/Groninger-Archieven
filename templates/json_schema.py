json_schema = """
Respond **ONLY** in valid JSON format, according to the following JSON schema:
  {
    "name": "",
    "jobTitle": "",
    "address": ""
  },
    "required": ["name", "jobTitle", "address"],
    "additionalProperties": false
  }


Do NOT include the schema in your reply. Do NOT include any additional text outside of the JSON object.
"""