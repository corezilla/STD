# EX-EXPORT 完整字段与签名阅读视图

<!-- Document ID: EX-EXPORT-CONTRACT-VIEW -->
<!-- Document Version: 3.0.0-draft.1 -->
<a id="contract-view"></a>

此页为机器源的确定性完整投影，不独立手改字段。先读[用途和行为](../mechanism-side-effect-example.md)，
再按[成员目录](README.md)定位；JSON 的 `$ref` 指向同一 Schema 的 `$defs`，不是未定义类型。
逻辑 JSON 对象没有固定 wire offset/Host sizeof；required 表示必填，未声明 default 表示无缺省，
null 只有明确列入时才合法。额外键禁止；字节上限、关联与跨字段行为另按正文/模型核查。

## IF-EXPORT#TYPE01 · Id

<!-- CONTRACT_VIEW IF-EXPORT#TYPE01 BEGIN -->
```json
{
  "$comment": "1–64 ASCII characters; opaque identity, not credentials; no default/null",
  "pattern": "^[A-Za-z][A-Za-z0-9-]{0,63}$",
  "type": "string"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE01 END -->

## IF-EXPORT#TYPE02 · Payload

<!-- CONTRACT_VIEW IF-EXPORT#TYPE02 BEGIN -->
```json
{
  "$comment": "Frozen input, empty allowed; <=4096 UTF-8 bytes (byte bound needs encoding check); no implicit conversion or appended LF.",
  "maxLength": 4096,
  "type": "string",
  "x-max-utf8-bytes": 4096
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE02 END -->

## IF-EXPORT#TYPE03 · EmptyArgs

<!-- CONTRACT_VIEW IF-EXPORT#TYPE03 BEGIN -->
```json
{
  "additionalProperties": false,
  "properties": {},
  "required": [],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE03 END -->

## IF-EXPORT#TYPE04 · PrepareArgs

<!-- CONTRACT_VIEW IF-EXPORT#TYPE04 BEGIN -->
```json
{
  "additionalProperties": false,
  "properties": {
    "payload": {
      "$ref": "#/$defs/Payload"
    },
    "slot_id": {
      "$comment": "Only teaching slot; ownership remains A",
      "const": "slot-1"
    }
  },
  "required": [
    "slot_id",
    "payload"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE04 END -->

## IF-EXPORT#TYPE05 · FinalizeArgs

<!-- CONTRACT_VIEW IF-EXPORT#TYPE05 BEGIN -->
```json
{
  "additionalProperties": false,
  "properties": {
    "disposition": {
      "$comment": "Explicit selected branch; immutable after finalize",
      "enum": [
        "deliver",
        "discard"
      ]
    }
  },
  "required": [
    "disposition"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE05 END -->

## IF-EXPORT#TYPE06 · State

<!-- CONTRACT_VIEW IF-EXPORT#TYPE06 BEGIN -->
```json
{
  "$comment": "All fields required; separate five-axis meanings and legal transitions at prose EX-R1–8; no implicit defaults.",
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "phase": {
            "enum": [
              "STOPPED",
              "FINALIZED",
              "RELEASED"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "access": {
            "const": "FENCED"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "phase": {
            "enum": [
              "FINALIZED",
              "RELEASED"
            ]
          }
        }
      },
      "then": {
        "properties": {
          "disposition": {
            "enum": [
              "deliver",
              "discard"
            ]
          },
          "evidence": {
            "enum": [
              "CAPTURED",
              "UNRECOVERABLE"
            ]
          }
        }
      }
    },
    {
      "else": {
        "properties": {
          "admission": {
            "const": "BLOCKED"
          },
          "resource": {
            "const": "HELD"
          }
        }
      },
      "if": {
        "properties": {
          "phase": {
            "const": "RELEASED"
          }
        }
      },
      "then": {
        "properties": {
          "admission": {
            "const": "ELIGIBLE"
          },
          "resource": {
            "const": "RELEASED"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "phase": {
            "const": "PREPARED"
          }
        }
      },
      "then": {
        "properties": {
          "access": {
            "const": "OPEN"
          },
          "disposition": {
            "type": "null"
          },
          "evidence": {
            "const": "PENDING"
          },
          "result": {
            "const": "NOT_STARTED"
          }
        }
      }
    }
  ],
  "properties": {
    "access": {
      "enum": [
        "OPEN",
        "CLOSING",
        "FENCED"
      ]
    },
    "admission": {
      "enum": [
        "BLOCKED",
        "ELIGIBLE"
      ]
    },
    "disposition": {
      "enum": [
        null,
        "deliver",
        "discard"
      ]
    },
    "evidence": {
      "enum": [
        "PENDING",
        "CAPTURED",
        "UNRECOVERABLE"
      ]
    },
    "phase": {
      "enum": [
        "PREPARED",
        "EXECUTING",
        "STOPPING",
        "STOPPED",
        "FINALIZED",
        "RELEASED"
      ]
    },
    "resource": {
      "enum": [
        "HELD",
        "RELEASED"
      ]
    },
    "result": {
      "enum": [
        "NOT_STARTED",
        "UNKNOWN",
        "SUCCEEDED",
        "FAILED"
      ]
    }
  },
  "required": [
    "phase",
    "result",
    "access",
    "evidence",
    "disposition",
    "resource",
    "admission"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE06 END -->

## IF-EXPORT#TYPE07 · Output

<!-- CONTRACT_VIEW IF-EXPORT#TYPE07 BEGIN -->
```json
{
  "$comment": "Validate decoded <=4096 bytes, SHA-256 and equality to frozen payload UTF-8; schema alone cannot prove these.",
  "additionalProperties": false,
  "properties": {
    "data": {
      "maxLength": 5464,
      "pattern": "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
      "type": "string"
    },
    "encoding": {
      "const": "base64"
    },
    "sha256": {
      "pattern": "^[0-9a-f]{64}$",
      "type": "string"
    }
  },
  "required": [
    "encoding",
    "data",
    "sha256"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE07 END -->

## IF-EXPORT#TYPE08 · Request

<!-- CONTRACT_VIEW IF-EXPORT#TYPE08 BEGIN -->
```json
{
  "$comment": "No unknown/duplicate keys; JSON Lines <=8192 bytes; UID is authenticated via peer credentials, not payload.",
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "op": {
            "const": "prepare"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/PrepareArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "execute"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/EmptyArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "inspect"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/EmptyArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "stop"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/EmptyArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "collect"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/EmptyArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "finalize"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/FinalizeArgs"
          }
        }
      }
    },
    {
      "if": {
        "properties": {
          "op": {
            "const": "release"
          }
        }
      },
      "then": {
        "properties": {
          "args": {
            "$ref": "#/$defs/EmptyArgs"
          }
        }
      }
    }
  ],
  "properties": {
    "agent_instance": {
      "$ref": "#/$defs/Id"
    },
    "args": {
      "oneOf": [
        {
          "$ref": "#/$defs/PrepareArgs"
        },
        {
          "$ref": "#/$defs/FinalizeArgs"
        },
        {
          "$ref": "#/$defs/EmptyArgs"
        }
      ]
    },
    "op": {
      "enum": [
        "prepare",
        "execute",
        "inspect",
        "stop",
        "collect",
        "finalize",
        "release"
      ]
    },
    "operation_id": {
      "$ref": "#/$defs/Id"
    },
    "protocol": {
      "const": "EX-EXPORT-01/v1"
    },
    "request_id": {
      "$ref": "#/$defs/Id"
    }
  },
  "required": [
    "protocol",
    "request_id",
    "agent_instance",
    "operation_id",
    "op",
    "args"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE08 END -->

## IF-EXPORT#TYPE09 · Error

<!-- CONTRACT_VIEW IF-EXPORT#TYPE09 BEGIN -->
```json
{
  "additionalProperties": false,
  "properties": {
    "code": {
      "enum": [
        "FORBIDDEN",
        "BAD_REQUEST",
        "INSTANCE_MISMATCH",
        "NOT_FOUND",
        "CLOSED",
        "CONFLICT",
        "BUSY",
        "LEDGER_FULL",
        "NOT_SAFE",
        "EVIDENCE_PENDING",
        "RESULT_UNAVAILABLE",
        "NOT_FINALIZED"
      ]
    }
  },
  "required": [
    "code"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE09 END -->

## IF-EXPORT#TYPE10 · SuccessResponse

<!-- CONTRACT_VIEW IF-EXPORT#TYPE10 BEGIN -->
```json
{
  "$comment": "<=16384 bytes; correlate all four identity fields to current request. Output only for successful/repeated finalize(deliver); cannot establish this from response alone.",
  "additionalProperties": false,
  "allOf": [
    {
      "if": {
        "properties": {
          "output": {
            "type": "object"
          }
        }
      },
      "then": {
        "properties": {
          "state": {
            "properties": {
              "disposition": {
                "const": "deliver"
              },
              "evidence": {
                "const": "CAPTURED"
              },
              "phase": {
                "enum": [
                  "FINALIZED",
                  "RELEASED"
                ]
              },
              "result": {
                "const": "SUCCEEDED"
              }
            }
          }
        }
      }
    }
  ],
  "properties": {
    "agent_instance": {
      "$ref": "#/$defs/Id"
    },
    "ok": {
      "const": true
    },
    "operation_id": {
      "$ref": "#/$defs/Id"
    },
    "output": {
      "oneOf": [
        {
          "$ref": "#/$defs/Output"
        },
        {
          "type": "null"
        }
      ]
    },
    "protocol": {
      "const": "EX-EXPORT-01/v1"
    },
    "request_id": {
      "$ref": "#/$defs/Id"
    },
    "state": {
      "$ref": "#/$defs/State"
    }
  },
  "required": [
    "protocol",
    "request_id",
    "agent_instance",
    "operation_id",
    "ok",
    "state",
    "output"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE10 END -->

## IF-EXPORT#TYPE11 · ErrorResponse

<!-- CONTRACT_VIEW IF-EXPORT#TYPE11 BEGIN -->
```json
{
  "$comment": "Unparseable correlation fields null; state/output absent. Errors and connection uncertainty follow prose, not automatic retry.",
  "additionalProperties": false,
  "properties": {
    "agent_instance": {
      "oneOf": [
        {
          "$ref": "#/$defs/Id"
        },
        {
          "type": "null"
        }
      ]
    },
    "error": {
      "$ref": "#/$defs/Error"
    },
    "ok": {
      "const": false
    },
    "operation_id": {
      "oneOf": [
        {
          "$ref": "#/$defs/Id"
        },
        {
          "type": "null"
        }
      ]
    },
    "protocol": {
      "const": "EX-EXPORT-01/v1"
    },
    "request_id": {
      "oneOf": [
        {
          "$ref": "#/$defs/Id"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "protocol",
    "request_id",
    "agent_instance",
    "operation_id",
    "ok",
    "error"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE11 END -->

## IF-EXPORT#TYPE12 · Response

<!-- CONTRACT_VIEW IF-EXPORT#TYPE12 BEGIN -->
```json
{
  "oneOf": [
    {
      "$ref": "#/$defs/SuccessResponse"
    },
    {
      "$ref": "#/$defs/ErrorResponse"
    }
  ]
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE12 END -->

## IF-EXPORT#TYPE13 · CompletionReceipt

<!-- CONTRACT_VIEW IF-EXPORT#TYPE13 BEGIN -->
```json
{
  "$comment": "Internal A/W receipt, not new C→A operation; binds FIRST execute request_id and frozen payload. Ingress closes atomically with fencing per EX-R5.",
  "additionalProperties": false,
  "allOf": [
    {
      "else": {
        "properties": {
          "output": {
            "$ref": "#/$defs/Output"
          }
        }
      },
      "if": {
        "properties": {
          "result": {
            "const": "FAILED"
          }
        }
      },
      "then": {
        "properties": {
          "output": {
            "type": "null"
          }
        }
      }
    }
  ],
  "properties": {
    "agent_instance": {
      "$ref": "#/$defs/Id"
    },
    "operation_id": {
      "$ref": "#/$defs/Id"
    },
    "output": {
      "oneOf": [
        {
          "$ref": "#/$defs/Output"
        },
        {
          "type": "null"
        }
      ]
    },
    "payload_sha256": {
      "pattern": "^[0-9a-f]{64}$",
      "type": "string"
    },
    "protocol": {
      "const": "EX-EXPORT-01/v1"
    },
    "request_id": {
      "$ref": "#/$defs/Id"
    },
    "result": {
      "enum": [
        "SUCCEEDED",
        "FAILED"
      ]
    },
    "slot_id": {
      "const": "slot-1"
    }
  },
  "required": [
    "protocol",
    "request_id",
    "agent_instance",
    "operation_id",
    "slot_id",
    "payload_sha256",
    "result",
    "output"
  ],
  "type": "object"
}
```
<!-- CONTRACT_VIEW IF-EXPORT#TYPE13 END -->

## IF-EXPORT#OP01 · prepare

<!-- CONTRACT_VIEW IF-EXPORT#OP01 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/PrepareArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP01",
  "mode": "synchronous-control",
  "name": "prepare",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP01 END -->

## IF-EXPORT#OP02 · execute

<!-- CONTRACT_VIEW IF-EXPORT#OP02 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/EmptyArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP02",
  "mode": "synchronous-control",
  "name": "execute",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP02 END -->

## IF-EXPORT#OP03 · inspect

<!-- CONTRACT_VIEW IF-EXPORT#OP03 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/EmptyArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP03",
  "mode": "synchronous-control",
  "name": "inspect",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP03 END -->

## IF-EXPORT#OP04 · stop

<!-- CONTRACT_VIEW IF-EXPORT#OP04 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/EmptyArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP04",
  "mode": "synchronous-control",
  "name": "stop",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP04 END -->

## IF-EXPORT#OP05 · collect

<!-- CONTRACT_VIEW IF-EXPORT#OP05 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/EmptyArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP05",
  "mode": "synchronous-control",
  "name": "collect",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP05 END -->

## IF-EXPORT#OP06 · finalize

<!-- CONTRACT_VIEW IF-EXPORT#OP06 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/FinalizeArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP06",
  "mode": "synchronous-control",
  "name": "finalize",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP06 END -->

## IF-EXPORT#OP07 · release

<!-- CONTRACT_VIEW IF-EXPORT#OP07 BEGIN -->
```json
{
  "$comment": "Behavior, check order, legal errors and next calls: EX-EXPORT prose §4.2 / EX-R1–8; accepted != completed. op must equal name.",
  "args": {
    "$ref": "#/$defs/EmptyArgs"
  },
  "consumer": "C",
  "id": "IF-EXPORT#OP07",
  "mode": "synchronous-control",
  "name": "release",
  "provider": "A",
  "request": {
    "$ref": "#/$defs/Request"
  },
  "response": {
    "$ref": "#/$defs/Response"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#OP07 END -->

## IF-EXPORT#ERR01 · FORBIDDEN

<!-- CONTRACT_VIEW IF-EXPORT#ERR01 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "FORBIDDEN",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR01 END -->

## IF-EXPORT#ERR02 · BAD_REQUEST

<!-- CONTRACT_VIEW IF-EXPORT#ERR02 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "BAD_REQUEST",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR02 END -->

## IF-EXPORT#ERR03 · INSTANCE_MISMATCH

<!-- CONTRACT_VIEW IF-EXPORT#ERR03 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "INSTANCE_MISMATCH",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR03 END -->

## IF-EXPORT#ERR04 · NOT_FOUND

<!-- CONTRACT_VIEW IF-EXPORT#ERR04 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "NOT_FOUND",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR04 END -->

## IF-EXPORT#ERR05 · CLOSED

<!-- CONTRACT_VIEW IF-EXPORT#ERR05 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "CLOSED",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR05 END -->

## IF-EXPORT#ERR06 · CONFLICT

<!-- CONTRACT_VIEW IF-EXPORT#ERR06 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "CONFLICT",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR06 END -->

## IF-EXPORT#ERR07 · BUSY

<!-- CONTRACT_VIEW IF-EXPORT#ERR07 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "BUSY",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR07 END -->

## IF-EXPORT#ERR08 · LEDGER_FULL

<!-- CONTRACT_VIEW IF-EXPORT#ERR08 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "LEDGER_FULL",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR08 END -->

## IF-EXPORT#ERR09 · NOT_SAFE

<!-- CONTRACT_VIEW IF-EXPORT#ERR09 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "NOT_SAFE",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR09 END -->

## IF-EXPORT#ERR10 · EVIDENCE_PENDING

<!-- CONTRACT_VIEW IF-EXPORT#ERR10 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "EVIDENCE_PENDING",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR10 END -->

## IF-EXPORT#ERR11 · RESULT_UNAVAILABLE

<!-- CONTRACT_VIEW IF-EXPORT#ERR11 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "RESULT_UNAVAILABLE",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR11 END -->

## IF-EXPORT#ERR12 · NOT_FINALIZED

<!-- CONTRACT_VIEW IF-EXPORT#ERR12 BEGIN -->
```json
{
  "$comment": "Meaning and legal next action at prose error-actions; never infer no side effects from a missing response.",
  "code": "NOT_FINALIZED",
  "domain": "EX-EXPORT-01/v1",
  "response": {
    "$ref": "#/$defs/ErrorResponse"
  }
}
```
<!-- CONTRACT_VIEW IF-EXPORT#ERR12 END -->
