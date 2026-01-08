import ollama
import os
import fitz  # PyMuPDF

# ==========================================
# 👇 1. WHERE ARE YOUR FILES? (INPUT)
INPUT_FOLDER = r"C:\Users\emper\OneDrive\Desktop\Coding\PythonCode\text recog\data"

# 👇 2. WHERE SHOULD THE REPORT GO? (OUTPUT)
OUTPUT_FOLDER = r"C:\Users\emper\OneDrive\Desktop\Coding\PythonCode\text recog\Output"

# 👇 3. WHAT SHOULD THE FILE BE CALLED?
OUTPUT_FILE = "final_summary.md"
# ==========================================

MODEL_NAME = "llama3.2-vision"

def analyze_image(image_bytes, source_name):
    print(f"   👀 Llama is reading: {source_name}...")
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{
                'role': 'user',
                'content': 'Analyze this image. List the key points and data found in it.',
                'images': [image_bytes]
            }]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def create_master_summary(all_notes):
    print("\n🧠 Writing final Master Summary...")
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{
                'role': 'user',
                'content': f"Here are notes from several documents. Write a clear, combined summary of everything.\n\nNOTES:\n{all_notes}"
            }]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # 1. Check Input Folder
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ Error: Input folder missing: {INPUT_FOLDER}")
        return

    # 2. Check/Create Output Folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"📂 Created output folder: {OUTPUT_FOLDER}")

    # 3. Find files
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.pdf', '.jpg', '.png'))]
    if not files:
        print(f"❌ No files found in input folder.")
        return

    print(f"🚀 Found {len(files)} files. Starting processing...")
    all_notes = []

    # 4. Process each file
    for filename in files:
        filepath = os.path.join(INPUT_FOLDER, filename)
        
        if filename.lower().endswith('.pdf'):
            doc = fitz.open(filepath)
            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                note = analyze_image(img_bytes, f"{filename} (Page {i+1})")
                all_notes.append(f"--- {filename} Page {i+1} ---\n{note}")
        else:
            with open(filepath, "rb") as f:
                img_bytes = f.read()
            note = analyze_image(img_bytes, filename)
            all_notes.append(f"--- {filename} ---\n{note}")

    # 5. Save Report to the Fixed Output Folder
    final_output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    final_report = create_master_summary("\n".join(all_notes))
    
    with open(final_output_path, "w", encoding="utf-8") as f:
        f.write("# MASTER SUMMARY\n\n" + final_report)
    
    print(f"\n✅ Success! Report saved to:\n   {final_output_path}")

if __name__ == "__main__":
    main()