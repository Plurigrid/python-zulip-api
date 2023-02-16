from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
import os
import base64

# import gradio as gr
import cosmwasm


class Agent:
    def init(self):
        self.subdao = os.getenv("SUBDAO")
        template = "{history}{mw_input}"
        mw_prompt = PromptTemplate(input_variables=["history", "mw_input"], template=template)

        self.mw_chain = LLMChain(
            llm=OpenAI(temperature=0),
            prompt=mw_prompt,
            verbose=True,
            memory=ConversationalBufferWindowMemory(k=2),
        )

        mw_learnings = """
  Whenever I say "Microworld Update:" followed by a description of the aesthetic, modify the following message
  with the hexadecimal color value and brightness value that may best represent the mood and vibes of the specification.
  Include specification string itself instead of <specification> into the title field. The output must be valid JSON.

  {
    "microworld": {
    "propose": {
      "msg": {
        "propose": {
          "title": "<specification>",
          "description": "'brightness': '<brightness-value>', 'color': '<hexadecimal-color-value>'",
          "msgs": []
        }
      }
    }
  }
  }

  Please make sure to only edit brightness and color and keep the message structure in tact.

  For example:

  Input: shadowy supercoder
  Output: 
  {
    "microworld":
  {
    "propose": {
      "msg": {
        "propose": {
          "title": "shadowy supercoder",
          "description": "'brightness': 40, color: '#333333'",
          "msgs": []
        }
      }
    }
  }
  }

  Input: luxury space gay communism
  Output: 
  {
    "microworld":
  {
    "propose": {
      "msg": {
        "propose": {
          "title": "luxury space gay communism",
          "description": "'brightness': '100', 'color': '#C0C0C0'",
          "msgs": []
        }
      }
    }
  }
}

  And whenever I say things like:

  - include juno9000 into DAO
  - add to Plurigrid juno9000
  - + juno9000 to DAO
  - juno9000 add plzzzz
  - Add my address juno9000 to the DAO

  and similar things, where "juno9000" is the address of the member to be added,
  I want you to output the following message:
  {"members": add_members_msg = {
      "update_members": {
          "add": [{"weight": 1, "addr": "<addr>"}],
          "remove": [],
      }
  }

  Make sure you only modify the <addr> field and the rest of the message remains the same.

  Thanks!
  """

        self.mw_chain.predict(mw_input=mw_learnings)

    async def execute_cosmwasm(self, your_microworld_aesthetic):
        subdao = os.getenv("SUBDAO")
        print(your_microworld_aesthetic)
        msg = self.mw_chain.predict(
            mw_input="Microworld Update: {}".format(your_microworld_aesthetic)
        )
        print(msg)
        try:
            await cosmwasm.execute_msg(msg)
        except Exception as e:
            print(e)
            return "CosmWasm message not valid, giving up. Try again with a different wording."
        return (
            "View your proposal here!: https://daodao.zone/dao/{subdao}#proposals\n".format(
                subdao=subdao
            )
            + msg
        )

    async def handle_query(self, message):
        msg = self.mw_chain.predict(mw_input=message)
        # return self.execute_cosmwasm(self.format_add_member_msg(msg))
        print(msg)

    def format_add_member_msg(self, llm_response):
        response_bytes = llm_response.encode("ascii")
        base64_bytes = base64.b64encode(response_bytes)
        base64_msg = base64_bytes.decode("ascii")

        msg = """
  {
      "propose": {
          "msg": {
              "propose": {
                  "title": "Add member to a DAO",
                  "description": "Adding a new member",
                  "msgs": [
                      {
                          "wasm": {
                              "execute": {
                                  "contract_addr": "%s",
                                  "funds": [],
                                  "msg": "%s"
                              }
                          }
                      }
                  ]
              }
          }
      }
  }
  """ % (
            self.subdao,
            base64_msg,
        )
        return msg
