from agenticAiLab.callingGenAiApis.day2_LlmAsAJudge import chat
import gradio as gr


gr.ChatInterface(
    fn=chat,
).launch()
