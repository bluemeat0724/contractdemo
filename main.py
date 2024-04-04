import streamlit as st
import docx2txt

from chains import contract_info_chain, amount_convert_chain
from contract_service import validate_date_expire
from utils.date_converter import pares_json

st.title("技术合同审核Demo")
st.caption("验证合同金额和日期是否符合规范")

upload_file = st.file_uploader("上传合同文件", type=['pdf', 'docx', 'doc'])

if upload_file:
    doc_text = docx2txt.process(upload_file)
    with st.expander("查看合同文本"):
        st.text(doc_text)
    with st.spinner('读取合同信息中...'):
        contract_info = contract_info_chain.invoke(doc_text)

    with st.expander("查看合同关键信息"):
        st.json(contract_info)

    with st.spinner('合同审核...'):
        contract_info = pares_json(contract_info, ['合同开始期限', '合同结束期限'])
        check = ''
        amount_check = amount_convert_chain.invoke(
            {'chinese_amount': contract_info['合同中文大写金额']})
        print(amount_check)
        if amount_check['合同中文大写金额'] != contract_info['合同数字金额']:
            check += f"合同金额不匹配 请检查\n 数字金额: {contract_info['合同数字金额']}\n 中文金额: {contract_info['合同中文大写金额']}\n\n"
        check += validate_date_expire(contract_info['合同结束期限']) + '\n\n'

        st.text(check)
