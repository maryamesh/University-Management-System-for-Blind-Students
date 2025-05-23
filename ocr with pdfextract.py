import fitz  # PyMuPDF
import os
import pypdfium2
from PIL import Image
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor
from texify.output import replace_katex_invalid
from sympy.parsing.latex import parse_latex
import sympy as sp
import re

def extract_images_from_pdf(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    doc = fitz.open(pdf_path)
    image_paths = []
    
    for page_number in range(len(doc)):
        for img_index, img in enumerate(doc[page_number].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}"
            image_filepath = os.path.join(output_folder, image_filename)
            
            with open(image_filepath, "wb") as img_file:
                img_file.write(image_bytes)
            
            image_paths.append(image_filepath)
            print(f"Extracted: {image_filename}")
    
    print("Image extraction completed.")
    return image_paths

def load_image(image_path):
    return Image.open(image_path).convert("RGB")

def infer_whole_image(model, processor, pil_image, temperature=0.0):
    output = batch_inference([pil_image], model, processor, temperature=temperature)
    return output[0]

def extract_math_latex(latex_str):
    if "$" in latex_str:
        math_part = latex_str.split("$")[1:-1]
        return "".join(math_part)
    return latex_str

def latex_to_text(latex_str):
    try:
        math_latex = extract_math_latex(latex_str)
        expr = parse_latex(math_latex)
        return str(expr).replace("{", "").replace("}", "")
    except Exception as e:
        return f"Error parsing LaTeX: {str(e)}"

def equation_to_speech(equation):
    lhs, rhs = equation.lhs, equation.rhs
    spoken_lhs = expression_to_speech(lhs)
    spoken_rhs = expression_to_speech(rhs)
    return f"{spoken_lhs} is equal to {spoken_rhs}"

def expression_to_speech(expr):
    if expr.func == sp.log:
        return f"the natural logarithm of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.sqrt:
        return f"the square root of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.sin:
        return f"sine of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.cos:
        return f"cosine of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.tan:
        return f"tangent of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.exp:
        return f"e raised to the power of {expression_to_speech(expr.args[0])}"
    elif expr.func == sp.Mul and any(arg.func == sp.Pow and arg.args[1] == -1 for arg in expr.args):
        num = [arg for arg in expr.args if not (arg.func == sp.Pow and arg.args[1] == -1)]
        den = [arg.args[0] for arg in expr.args if arg.func == sp.Pow and arg.args[1] == -1]
        num_expr = sp.Mul(*num) if len(num) > 1 else num[0]
        den_expr = sp.Mul(*den) if len(den) > 1 else den[0]
        return f"{expression_to_speech(num_expr)} divided by {expression_to_speech(den_expr)}"
    elif expr.func == sp.Rational:
        return f"{expr.p} divided by {expr.q}"
    elif expr.func == sp.Mul:
        return " times ".join(expression_to_speech(arg) for arg in expr.args)
    elif expr.func == sp.Add:
        return " plus ".join(expression_to_speech(arg) for arg in expr.args)
    elif expr.func == sp.Pow:
        base, exp = expr.args
        return f"{expression_to_speech(base)} raised to the power of {expression_to_speech(exp)}"
    elif isinstance(expr, sp.Symbol):
        return str(expr).replace("_", " ").replace("beta", "beta ")
    elif isinstance(expr, sp.Number):
        return str(expr)
    else:
        return str(expr)

def parse_equation(equation_str):
    try:
        allowed_functions = {"Eq": sp.Eq, "log": sp.log, "sqrt": sp.sqrt, "exp": sp.exp,
                             "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "E": sp.exp(1)}
        symbol_matches = re.findall(r'[A-Za-z_][A-Za-z0-9_]*', equation_str)
        symbol_dict = {symbol: sp.Symbol(symbol) for symbol in set(symbol_matches) if symbol not in allowed_functions}
        safe_dict = {**allowed_functions, **symbol_dict}
        equation_str = re.sub(r'log\(([^,]+),\s*E\)', r'log(\1) / log(E)', equation_str)
        equation = eval(equation_str, safe_dict)
        if isinstance(equation, sp.Equality):
            return equation_to_speech(equation)
        else:
            return expression_to_speech(equation)
    except Exception as e:
        return f"Error: {e}. Invalid mathematical equation."

def main():
    pdf_path = "C:\\Users\\Dell\\OneDrive\\Desktop\\New Microsoft Word Document.pdf"  # Change this
    output_folder = "C:\\Users\\Dell\\OneDrive\\Desktop\\extracted_images"
    image_paths = extract_images_from_pdf(pdf_path, output_folder)
    
    if not image_paths:
        print("No images extracted.")
        return
    
    model = load_model()
    processor = load_processor()
    
    for image_path in image_paths:
        pil_image = load_image(image_path)
        inference = infer_whole_image(model, processor, pil_image, temperature=0.0)
        latex_text = replace_katex_invalid(inference)
        readable_text = latex_to_text(latex_text)
        spoken_equation = parse_equation(readable_text)
        
        print(f"Processing {image_path}")
        print("Spoken Form:")
        print(spoken_equation)

if __name__ == "__main__":
    main()
