import re
import textwrap
import tempfile
from typing import List

from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline


def _split_sentences(text: str) -> List[str]:
    """Simple sentence splitter."""
    return [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]


def extract_audio(video_path: str) -> str:
    """Extract audio track from video and return path to wav file."""
    clip = VideoFileClip(video_path)
    audio_path = f"{video_path}.wav"
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio using OpenAI Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"].strip()


def summarize_text(text: str, max_words: int = 200) -> str:
    """Summarize text using a Transformer model."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Roughly convert words to tokens (~1.33 tokens per word)
    max_len = int(max_words * 1.5)
    summary = summarizer(text, max_length=max_len, min_length=int(max_len * 0.7), do_sample=False)[0]["summary_text"]
    return summary.strip()


def generate_linkedin_post(summary: str) -> str:
    sentences = _split_sentences(summary)
    intro = sentences[0] if sentences else "Kurzer Überblick zum Video:"  # fallback
    bullets = sentences[1:4]
    cta = "Was haltet ihr davon? Schreibt es in die Kommentare!"
    bullet_text = "\n".join(f"- {b}" for b in bullets)
    return f"{intro}\n\n{bullet_text}\n\n{cta}"


def generate_twitter_thread(summary: str) -> List[str]:
    parts = textwrap.wrap(summary, width=240)
    total = len(parts)
    return [f"{i+1}/{total} {p}" for i, p in enumerate(parts)]


def generate_newsletter(summary: str) -> str:
    sentences = _split_sentences(summary)
    intro = " ".join(sentences[:2])
    main = " ".join(sentences[2:-2])
    outlook = " ".join(sentences[-2:])
    return f"{intro}\n\n{main}\n\nAusblick: {outlook}"


def process_video_file(upload_file) -> dict:
    """Full pipeline: video -> posts."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(upload_file)
        tmp_path = tmp.name
    audio_path = extract_audio(tmp_path)
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript)
    linkedin_post = generate_linkedin_post(summary)
    twitter_thread = generate_twitter_thread(summary)
    newsletter = generate_newsletter(summary)
    return {
        "transcript": transcript,
        "summary": summary,
        "linkedin_post": linkedin_post,
        "twitter_thread": twitter_thread,
        "newsletter": newsletter,
    }
