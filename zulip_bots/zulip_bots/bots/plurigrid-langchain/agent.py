from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory

# import gradio as gr
import cosmwasm


template = "{history}{mw_input}"
human_input = ""

mw_prompt = PromptTemplate(input_variables=["history", "mw_input"], template=template)

mw_chain = LLMChain(
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

Please make sure to only edit brightness and color and keep the message structure in tact.

For example:

Input: shadowy supercoder
Output: 
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

Input: luxury space gay communism
Out
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

And whenever I say things like:

- include juno9000 into DAO
- add to Plurigrid juno9000
- + juno9000 to DAO
- juno9000 add plzzzz
- Add my address juno9000 to the DAO

and similar things, where "juno9000" is the address of the member to be added,
I want you to output the following message:
add_members_msg = {
     "update_members": {
        "add": [{"weight": 1, "addr": "<addr>"}],
         "remove": [],
     }
}

Make sure you only modify the <addr> field and the rest of the message remains the same.

Thanks!
"""

mw_chain.predict(mw_input=mw_learnings)

# retries = 0


async def output(your_microworld_aesthetic):
    print(your_microworld_aesthetic)
    msg = mw_chain.predict(mw_input="Microworld Update: {}".format(your_microworld_aesthetic))
    # if needed structurally edit with regex: msg_edited = re.sub("^AI:\s*", "", output)
    print(msg)
    # Retry cosmwasm msg automatically until valid
    try:
        await cosmwasm.execute_msg(msg)
    except Exception as e:
        print(e)
        # print("CosmWasm message not valid, retrying...")
        # retries += 1
        # if retries < 5:
        # await output(your_microworld_aesthetic)
        # else:
        print("CosmWasm message not valid, giving up.")
    return (
        "View your proposal here!: https://daodao.zone/dao/juno1jeq3xqkn9kypghjeqjnhsdlnjsltajm8r3s80tem3juxsjlfan3s2kzmsd#proposals\n"
        + msg
    )


async def test(message):
    msg = mw_chain.predict(mw_input=message)
    return msg


# demo = gr.Interface(fn=output, inputs="text", outputs="text", input_desc="Microworld vibe")
# demo.launch()
