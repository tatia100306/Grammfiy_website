import anthropic
import os
from django.shortcuts import render
from dotenv import load_dotenv

# Memuat API Key dari file .env
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def grammar_view(request):
    result = None
    user_text = ""
    
    if request.method == "POST":
        user_text = request.POST.get("text")
        
        # Prompt instruksi agar AI memberikan format yang mudah dibaca program
        prompt = (
            f"Please correct the grammar of this text: '{user_text}'. "
            "Return the response in this exact format: "
            "Original: [original text] | Corrected: [corrected text] | Explanation: [brief explanation]"
        )
        
        try:
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Memecah respon AI menjadi bagian-bagian (Parsing)
            raw_response = message.content[0].text
            parts = raw_response.split('|')
            
            result = {
                'original': parts[0].replace('Original:', '').strip(),
                'corrected': parts[1].replace('Corrected:', '').strip(),
                'explanation': parts[2].replace('Explanation:', '').strip(),
            }
        except Exception as e:
            # Jika API bermasalah atau token habis
            result = {
                'original': user_text,
                'corrected': "Error: Gagal terhubung ke AI",
                'explanation': "Pastikan CLAUDE_API_KEY sudah benar di file .env"
            }
            
    return render(request, 'grammar.html', {'result': result, 'user_text': user_text})

# Pastikan fungsi view lainnya (login, chat, quiz, progress) tetap ada di bawahnya
def login_view(request): return render(request, 'login.html')
def register_view(request): return render(request, 'register.html')
def chat_view(request): return render(request, 'chat.html')
def quiz_view(request): return render(request, 'quiz.html')
def progress_view(request): return render(request, 'progress.html')