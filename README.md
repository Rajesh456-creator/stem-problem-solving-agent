# STEM Problem-Solving AI Agent — Cloud-friendly version

## Live Demo

Try the deployed Streamlit application here:

**[Open STEM Problem-Solving AI Agent](https://stem-problem-solving-agent-zpeoqrvjw3qxenvnnqkfpq.streamlit.app)**

**Note:** The application requires access to a supported Hugging Face inference model. Availability depends on the account's provider access and remaining credits.

A beginner-friendly portfolio prototype with a Streamlit web UI, a hosted Hugging Face inference endpoint, Pydantic structured-output validation, and SymPy checks for selected symbolic mathematics.

## What it demonstrates

- Multi-step problem-solving flow: model draft → schema validation → deterministic symbolic check → formatted response.
- Hosted inference, so no local LLM weights are downloaded to your laptop.
- Structured response validation with Pydantic.
- SymPy checks for quadratic roots, derivatives, and simplification.
- A small browser interface built with Streamlit.
- Unit tests for deterministic mathematical tools.

**Limitations:** This is a portfolio prototype, not a production-grade agent. It does not use LangGraph in this cloud variant, and the model/API must be available to your account. Symbolic checks cover only a few cases and do not validate all explanatory text. Do not submit sensitive data to hosted inference.

## Requirements

- Python 3.10+
- Hugging Face account and access token with inference permissions
- Internet access for hosted model calls

Create/manage tokens at https://huggingface.co/settings/tokens. Keep your token private; never commit it to GitHub.

## Run locally without downloading a model

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Enter your token in the app sidebar. The token is used for the hosted inference request and is not saved by this app. Model availability and access policies can change; if the default model is unavailable, choose an available chat-completion model supported by your Hugging Face inference provider.

## Run tests

```bash
pytest -q
```

Tests do not need a token or hosted model.

## Deploy with Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open https://share.streamlit.io/ and create an app from the repository, selecting `app.py`.
3. For a public demo, avoid asking visitors to paste secrets where possible. A safer owner-managed deployment is to configure `HF_TOKEN` in Streamlit app Secrets and adapt the app to read `st.secrets["HF_TOKEN"]`. Never commit secrets to GitHub.
4. Check the inference provider's terms, model availability, quotas, and possible charges before sharing the app.

## Suggested GitHub description

`Cloud-friendly STEM problem-solving assistant with hosted LLM inference, Pydantic structured outputs, SymPy checks, and a Streamlit interface.`

## Resume wording — only after you have built and tested it

`Built a cloud-friendly STEM problem-solving prototype using Python, Streamlit, hosted LLM inference, Pydantic, and SymPy, with structured response validation and automated symbolic checks.`

Do not claim production deployment, advanced agent orchestration, or LangGraph experience based only on this variant.
