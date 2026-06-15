import json
import urllib.request


def call_syndic_api(user_question, network_context):
    try:
        context_str = json.dumps(network_context, ensure_ascii=False, indent=2)

        system_prompt = (
            "Você é o Síndico Virtual da GoodWe..."
            f"\n\nDados atuais da rede:\n{context_str}"
        )

        payload = json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]

    except Exception:
        raise RuntimeError("API failure")