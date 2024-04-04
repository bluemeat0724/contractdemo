import streamlit as st

from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(openai_api_key=st.secrets['moon_key'],
                 openai_api_base=st.secrets['moon_api_base'],
                 model='moonshot-v1-8k', temperature=0)

content_extract_system = """你是资深合同审核员，会根据合同文本提取合同关键信息。
合同信息可能存在错误，但不要尝试修正。提取关键信息需要忠于原始文本内容以用于后续验证。
提取合同的项目名称，合同类别，甲方名称，乙方名称，合同数字金额，合同中文大写金额，合同开始期限，合同结束期限 
合同类别可以为 技术开发合同，技术转让合同，技术咨询合同，技术服务合同 
将信息包含在markdown文本中 json块返回。如何文本并非合同，json返回空。
"""
contract_prompt_template = """{contract}\n【重要】注意遵循返回格式要求"""
contract_prompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=content_extract_system),
     HumanMessagePromptTemplate.from_template(contract_prompt_template)])

contract_info_chain = contract_prompt | llm | SimpleJsonOutputParser()

amount_convert_prompt = ChatPromptTemplate.from_messages(
    [SystemMessage(
        content="""合同中文大写金额转换为数字，以markdown文本返回json格式信息。格式如下：
        ```json
        {"合同中文大写金额":xx}
         ```
         无视币种和单位，只转换金额数字。
         
         """),
        HumanMessagePromptTemplate.from_template("合同中文大写金额: {chinese_amount}")])

amount_convert_chain = amount_convert_prompt | llm | SimpleJsonOutputParser()
