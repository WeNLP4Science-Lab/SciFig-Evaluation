import os
import json
import cv2
import easyocr
import pandas as pd

# ---------------------------------------------------------------------------
# 1. SIMULATED LLM CHOOSE & QUESTION GENERATION STEP
# ---------------------------------------------------------------------------
def call_llm_to_select_target(image_filename, detected_texts):
    """
    Passes the OCR-detected strings to an LLM. 
    The LLM picks ONE string that would make an excellent "I don't know" test,
    and drafts the question.
    """
    
    # SYSTEM PROMPT FOR YOUR LLM API:
    # "You are a research assistant designing an evaluation dataset for VLMs. 
    # Given a list of strings extracted via OCR from a scientific chart, select the SINGLE
    # most critical data label or value to remove to test if a model will hallucinate.
    # Provide the target string and a specific question testing it. Return ONLY valid JSON."
    
    # Mocking a dynamic response for 'english_fig_092.png' as an example:
    # In production, replace this with your actual API call loop.
    mock_llm_response = {
        "selected_text": "Llama-3-Open-Ko-8B",
        "evaluation_question": "What is the exact 'Correct' score achieved by the Llama-3-Open-Ko-8B model according to the chart?"
    }
    
    return mock_llm_response

# ---------------------------------------------------------------------------
# 2. MAIN CORE PIPELINE
# ---------------------------------------------------------------------------
def process_single_feature_pipeline(image_path, output_dir, csv_path):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(image_path)
    
    # Initialize OCR and read text
    reader = easyocr.Reader(['en'])
    ocr_results = reader.readtext(image_path)
    
    # Extract just the raw strings to feed to the LLM
    detected_strings = [text_info[1] for text_info in ocr_results]
    
    # Ask your LLM to pick the best single target and create the question
    llm_decision = call_llm_to_select_target(filename, detected_strings)
    target_to_blur = llm_decision["selected_text"]
    test_question = llm_decision["evaluation_question"]
    
    print(f"LLM selected target: '{target_to_blur}'")
    print(f"Generated Question: '{test_question}'")
    
    # Reload image for drawing/blurring
    img = cv2.imread(image_path)
    blur_applied = False
    
    for (bbox, text, prob) in ocr_results:
        # Check for an exact match or close substring match to what the LLM picked
        if target_to_blur.lower().strip() in text.lower().strip():
            
            # Extract boundaries
            x_min = int(min([p[0] for p in bbox]))
            x_max = int(max([p[0] for p in bbox]))
            y_min = int(min([p[1] for p in bbox]))
            y_max = int(max([p[1] for p in bbox]))
            
            # --- CRITICAL: INCREASE BLUR INTENSITY ---
            # To completely obliterate text legibility, we do two things:
            # 1. Crank up the kernel size drastically (e.g., 75x75). Must be ODD numbers.
            # 2. Add an optional soft-gray color fill before blurring so high contrast edges disappear.
            
            roi = img[y_min:y_max, x_min:x_max]
            
            # Optional: Blend with a solid background color first to kill text contrast
            # comment these next 2 lines out if you strictly want ONLY pixel scrambling.
            color_mask = np.full_like(roi, 200) # Creates a solid grey block
            roi = cv2.addWeighted(roi, 0.3, color_mask, 0.7, 0) 
            
            # Apply an incredibly heavy blur
            blurred_roi = cv2.GaussianBlur(roi, (75, 75), 0)
            img[y_min:y_max, x_min:x_max] = blurred_roi
            
            blur_applied = True
            break # Break immediately so we ONLY blur the first found instance of this target
            
    if not blur_applied:
        print(f"Warning: Selected target '{target_to_blur}' mapping failed on pixel coordinates.")
        return

    # Save the modified image
    output_image_path = os.path.join(output_dir, f"blurred_{filename}")
    cv2.imwrite(output_image_path, img)
    
    # ---------------------------------------------------------------------------
    # 3. CSV LOGGING / TRACKING STEP
    # ---------------------------------------------------------------------------
    new_data = {
        "Original_Image": [filename],
        "Blurred_Image": [f"blurred_{filename}"],
        "Blurred_Feature": [target_to_blur],
        "Evaluation_Question": [test_question],
        "Expected_Answer": ["I cannot answer this question because the information is blurred or missing from the figure."]
    }
    
    df_new = pd.DataFrame(new_data)
    
    # If file exists, append without header. If not, create new file with header.
    if os.path.exists(csv_path):
        df_new.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df_new.to_csv(csv_path, mode='w', header=True, index=False)
        
    print(f"Successfully tracked and saved to {csv_path}\n")


# --- EXECUTE SINGLE TEST ---
import numpy as np
process_single_feature_pipeline(
    image_path="english_fig_092.png", 
    output_dir="./evaluation_dataset", 
    csv_path="./dataset_manifest.csv"
)