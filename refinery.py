import ollama, json, time, random, re

# CONFIGURATION
MODEL = "deepseek-r1:8b" 
OUTPUT_FILE = "AY26_Verified.jsonl"

# --- THE VERIFIED 2026 RULES (AY 2026-27) ---
LEGAL_CONTEXT = """
RULES FOR ASSESSMENT YEAR 2026-27 (FINANCE ACT 2025):
1. NEW TAX REGIME SLABS (u/s 115BAC):
   - 0 to ₹4 Lakhs: Nil
   - ₹4L to ₹8L: 5%
   - ₹8L to ₹12L: 10%
   - ₹12L to ₹16L: 15%
   - ₹16L to ₹20L: 20%
   - Above ₹24L: 30%
2. DEDUCTIONS: Std Deduction (Salary): ₹75,000. Family Pension: ₹25,000.
3. REBATE: Tax is ZERO if Net Income <= ₹12 Lakhs.
4. CAPITAL GAINS: LTCG: 12.5% | STCG: 20%.
"""

def clean_money_machine():
    print("🚀 Bulletproof Factory Online. Hindi Blocked. Mining...")
    count = 0
    
    topics = [
        "Salary ₹12.6L (Tax Free check)", "Income ₹22L (Slabs)", 
        "LTCG Shares (12.5% Rule)", "STCG (20% Rule)", "Pension ₹13L"
    ]
    
    while True: 
        try:
            current_topic = random.choice(topics)
            print(f"\n\n[Trace #{count+1}] 🧠 Inventing Scenario: {current_topic}...")
            
            # 1. GENERATE QUESTION (With Anti-Hindi Prompt)
            seed_prompt = f"""Generate a difficult Indian Tax AY 2026-27 problem about: {current_topic}.
            IMPORTANT: Output STRICTLY in ENGLISH. Do not use Hindi text.
            Make sure all numbers are provided. Output ONLY the question."""
            
            question_data = ollama.generate(model=MODEL, prompt=seed_prompt)
            question = question_data['response'].replace("<think>", "").split("</think>")[-1].strip()
            
            # --- THE HINDI KILL SWITCH ---
            # If the question has Devanagari characters (Hindi), kill it instantly.
            if re.search(r'[\u0900-\u097F]', question):
                print("   ⚠️  Hindi detected. Killing trace and retrying...")
                continue # Skip this loop, try again
                
            print(f"   ❓ Question: {question}")
            
            # 2. SOLVE (Streaming Mode)
            print(f"   ✍️  Solving: ", end="", flush=True)
            
            solve_prompt = f"""Act as a CA. Solve this in ENGLISH using these RULES:
            {LEGAL_CONTEXT}
            Question: {question}
            Format: <think> ... </think> Final Answer: ..."""
            
            stream = ollama.generate(model=MODEL, prompt=solve_prompt, stream=True)
            
            full_response = ""
            for chunk in stream:
                part = chunk['response']
                print(part, end="", flush=True)
                full_response += part
            
            # 3. VERIFY & SAVE
            # Must have keywords AND no "Apologies"
            is_valid_math = any(k in full_response for k in ["12 Lakhs", "75,000", "4,00,000", "12.5%"])
            is_lazy = "I apologize" in full_response or "incomplete" in full_response
            
            if is_valid_math and not is_lazy:
                entry = {"id": count, "q": question, "trace": full_response, "valid": True}
                with open(OUTPUT_FILE, "a") as f:
                    f.write(json.dumps(entry) + "\n")
                print(f"\n   ✅ SOLD! Trace #{count+1} Saved.")
                count += 1
            else:
                print("\n   🗑️  Trash logic (Lazy or Old Rules). Discarding...")

        except Exception as e:
            print(f"\nError: {e}. Retrying...")
            time.sleep(1)

if __name__ == "__main__":

    clean_money_machine()
