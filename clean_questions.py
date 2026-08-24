"""
Post-processing cleaner for questions.json.
Strips garbled Unicode characters from PDF mis-encoding 
(Tamil, Malayalam, Oriya, Kannada, Telugu, Ethiopic scripts 
that appear when pypdf can't decode math font tables properly).
"""
import json
import re
import unicodedata

QUESTIONS_FILE = "app/data/questions.json"

# Unicode ranges for scripts commonly mis-used in PDF math fonts
GARBLED_RANGES = [
    (0x0B00, 0x0B7F),  # Oriya/Odia
    (0x0B80, 0x0BFF),  # Tamil
    (0x0C00, 0x0C7F),  # Telugu
    (0x0C80, 0x0CFF),  # Kannada
    (0x0D00, 0x0D7F),  # Malayalam
    (0x0D80, 0x0DFF),  # Sinhala
    (0x1200, 0x137F),  # Ethiopic
    (0x1380, 0x139F),  # Ethiopic Supplement
    (0x2C80, 0x2CFF),  # Coptic
    (0x0600, 0x06FF),  # Arabic (in formulas context)
    (0x0700, 0x074F),  # Syriac
]

def is_garbled(c):
    cp = ord(c)
    for lo, hi in GARBLED_RANGES:
        if lo <= cp <= hi:
            return True
    return False

# Common substitutions for math symbols that pypdf extracts as lookalike chars
SUBS = [
    # Math italic letters (𝑅𝑒𝑙𝑎𝑡𝑖𝑣𝑒 → Relative)
    # These are in Mathematical Alphanumeric Symbols block
    # Map them to ASCII equivalents
]

def clean_math_italics(text):
    """Convert Unicode mathematical italic letters to regular ASCII."""
    result = []
    for c in text:
        cp = ord(c)
        # Mathematical Italic capital letters: U+1D434–U+1D44D → A-Z
        if 0x1D434 <= cp <= 0x1D44D:
            result.append(chr(cp - 0x1D434 + ord('A')))
        # Mathematical Italic small letters: U+1D44E–U+1D467 → a-z
        elif 0x1D44E <= cp <= 0x1D467:
            result.append(chr(cp - 0x1D44E + ord('a')))
        # Mathematical Bold capital letters: U+1D400–U+1D419 → A-Z
        elif 0x1D400 <= cp <= 0x1D419:
            result.append(chr(cp - 0x1D400 + ord('A')))
        # Mathematical Bold small letters: U+1D41A–U+1D433 → a-z
        elif 0x1D41A <= cp <= 0x1D433:
            result.append(chr(cp - 0x1D41A + ord('a')))
        # Mathematical Sans-Serif: U+1D5A0–U+1D5B9, U+1D5BA–U+1D5D3
        elif 0x1D5A0 <= cp <= 0x1D5B9:
            result.append(chr(cp - 0x1D5A0 + ord('A')))
        elif 0x1D5BA <= cp <= 0x1D5D3:
            result.append(chr(cp - 0x1D5BA + ord('a')))
        else:
            result.append(c)
    return ''.join(result)

def clean_text(text):
    if not text:
        return text
    
    # Convert math italic/bold letters to ASCII first
    text = clean_math_italics(text)
    
    # Replace known garbled characters with space
    result = []
    for c in text:
        if is_garbled(c):
            result.append(' ')
        else:
            result.append(c)
    text = ''.join(result)
    
    # Fix common PDF extraction artifacts
    text = text.replace('\xa0', ' ')  # non-breaking space
    text = text.replace('\u200b', '')  # zero-width space
    text = text.replace('\u2060', '')  # word joiner
    text = text.replace('\ufeff', '')  # BOM
    
    # Fix em/en dashes
    text = text.replace('\u2013', '-').replace('\u2014', '-')
    text = text.replace('\u2212', '-')  # minus sign → hyphen
    
    # Fix smart quotes
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    
    # Fix multiplication/division signs to ASCII
    text = text.replace('\u00d7', 'x')  # × → x
    text = text.replace('\u00f7', '/')  # ÷ → /
    
    # Remove lines that are >40% garbage after cleaning
    lines = text.split('\n')
    good_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Count non-ASCII printable chars (possibly remaining garbage)
        non_ascii = sum(1 for c in stripped if ord(c) > 127)
        total = len(stripped)
        ratio = non_ascii / total if total > 0 else 0
        
        # Allow lines with some math symbols but not mostly garbage
        if ratio < 0.5 or total < 5:
            good_lines.append(stripped)
    
    text = ' '.join(good_lines)
    
    # Collapse multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove orphaned single characters that are clearly remnants (e.g. " . 0 s .")
    # Clean up isolated letters/numbers with spaces around them
    text = re.sub(r'\s+\.+\s+', '. ', text)
    
    return text

def clean_question(q):
    """Clean all text fields in a question."""
    q = dict(q)
    
    # Clean content (question stem)
    q['content'] = clean_text(q.get('content', ''))
    
    # Clean options
    q['options'] = [
        {'id': opt['id'], 'text': clean_text(opt['text'])}
        for opt in q.get('options', [])
    ]
    
    # Clean hints
    q['hints'] = [clean_text(h) for h in q.get('hints', [])]
    
    # Clean solution
    sol = dict(q.get('solution', {}))
    sol['summary'] = clean_text(sol.get('summary', ''))
    sol['steps'] = [clean_text(s) for s in sol.get('steps', [])]
    sol['formulasUsed'] = [clean_text(f) for f in sol.get('formulasUsed', [])]
    sol['keyTakeaway'] = clean_text(sol.get('keyTakeaway', ''))
    q['solution'] = sol
    
    return q

def main():
    print(f"Loading {QUESTIONS_FILE}...")
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"Cleaning {len(questions)} questions...")
    cleaned = [clean_question(q) for q in questions]
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    
    print(f"Done. Saved {len(cleaned)} questions.")
    
    # Show before/after for first 3 questions
    print("\n--- Sample cleaned solutions ---")
    for q in cleaned[:3]:
        print(f"\n{q['id']}:")
        print(f"  Summary: {q['solution']['summary'][:120]}")
        if q['solution']['steps']:
            print(f"  Step 1: {q['solution']['steps'][0][:120]}")

if __name__ == "__main__":
    main()
