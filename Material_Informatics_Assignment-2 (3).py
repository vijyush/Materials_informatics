#!/usr/bin/env python
# coding: utf-8

# ### DATASETS COLLECTION

# In[459]:


#### CHATGPT

import pandas as pd
import random
import numpy as np

# Define alloy base names
alloy_bases = [
    "AlCoCrFeNi", "CoCrFeMnNi", "AlCuLiMgAg", "CoCrFeNiPd", "FeCrMnNiCu",
    "CoCrFeNiTi", "CoCrFeNiAl", "FeCrMnNi", "CoCrFeMnNiV", "CrMnFeCoNi"
]

# Define ranges or possible values for each property
grain_sizes = [random.uniform(1, 50) for _ in range(60)]  # µm
phases = ["FCC", "Dual-phase", "L12 + FCC"]
dislocation_density_range = (1e13, 1e15)  # dislocations/m^2
temperatures = ["RT", "200°C", "400°C", "600°C", "-196°C"]
ys_range = (200, 1000)  # MPa
uts_range = (250, 1200)  # MPa
hardness_range = (100, 400)  # Vickers
elongation_range = (1, 70)  # %
strain_rate_options = [1e-3, 3e-4, 1e-4]
n_range = (0.1, 0.5)  # Strain hardening exponent
k_range = (200, 1000)  # Strain hardening coefficient (MPa)

# Simulate 60 data points
data = []
for i in range(60):
    composition = random.choice(alloy_bases) + f"_{random.randint(1, 10)*0.1:.1f}"
    processing = random.choice([
        "Arc-melted → Annealed",
        "Cast → Hot-rolled → Aged",
        "SLM → Annealed",
        "Magnetron sputtering → Annealed",
        "Vacuum induction melting → Hot-forged → Annealed"
    ])
    test_temp = random.choice(temperatures)
    phase = random.choice(phases)
    grain_size = round(grain_sizes[i], 2)
    dislocation_density = round(random.uniform(*dislocation_density_range), 2)
    ys = round(random.uniform(*ys_range), 1)
    uts = round(random.uniform(*uts_range), 1)
    hardness = round(random.uniform(*hardness_range), 1)
    elongation = round(random.uniform(*elongation_range), 1)
    strain_rate = random.choice(strain_rate_options)
    n = round(random.uniform(*n_range), 3)
    k = round(random.uniform(*k_range), 1)

    # Introduce deliberate missing values
    if random.random() < 0.1:
        elongation = None
    if random.random() < 0.1:
        hardness = None
    if random.random() < 0.05:
        dislocation_density = None
    if random.random() < 0.05:
        processing = None

    # Add inconsistencies
    if random.random() < 0.05:
        ys = str(ys) + " MPa"  # Unit inside string
    if random.random() < 0.05:
        test_temp = test_temp.lower()  # Inconsistent casing

    data.append({
        "Composition": composition,
        "Processing Condition": processing,
        "Test Temperature": test_temp,
        "Phase": phase,
        "Grain Size (µm)": grain_size,
        "Dislocation Density (dislocations/m²)": dislocation_density,
        "YS (MPa)": ys,
        "UTS (MPa)": uts,
        "Hardness (HV)": hardness,
        "Elongation (%)": elongation,
        "Strain Rate (s⁻¹)": strain_rate,
        "Strain Hardening Exponent (n)": n,
        "Strain Hardening Coefficient (k)": k
    })

df = pd.DataFrame(data)

df.to_csv("hea_data_chatgpt.csv",index=False)
df.head(60) 



# In[460]:


#claude
import pandas as pd
import re

def markdown_to_csv(input_file, output_file):
    # Read the markdown file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the table part (skip the title)
    table_start = content.find('|')
    if table_start == -1:
        raise ValueError("No table found in the input file")
    
    table_content = content[table_start:]
    
    # Split by lines
    lines = table_content.strip().split('\n')
    
    # Extract headers (first line)
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    
    # Skip the separator line (second line)
    data_lines = lines[2:]
    
    # Parse data rows
    data = []
    for line in data_lines:
        if '|' in line:  # Ensure it's a table row
            # Split by | and remove empty first and last elements
            row_values = [cell.strip() for cell in line.split('|')[1:-1]]
            data.append(row_values)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Export to CSV with UTF-8 encoding
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Successfully converted to CSV: {output_file}")
    
    return df

# Example usage
input_file = "hea_data.txt"  # Your input file with the markdown table
output_file = "hea_data_claude.csv"  # Output CSV file

# Save the table data to a text file first with UTF-8 encoding
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(""" # High Entropy Alloys (HEAs) Synthetic Dataset

| Composition | Processing Condition | Test Temperature | Phase | Grain Size (µm) | Dislocation Density (m⁻²) | YS (MPa) | UTS (MPa) | Hardness (HV) | Elongation (%) | Strain Rate (s⁻¹) | Strain Hardening Exponent (n) | Strain Hardening Coefficient (k) |
|-------------|---------------------|------------------|-------|-----------------|---------------------------|----------|-----------|---------------|----------------|-------------------|-------------------------------|----------------------------------|
| AlCoCrFeNi | Arc-melted → Annealed | rt | FCC | 25.3 | 3.4e14 | 387 | 642 | 217 | 38.5 | 0.001 | 0.32 | 412 |
| CoCrFeNi | Cast → Homogenized | rt | FCC | 18.7 | 1.8e14 | 241 | 479 | 185 | 45.2 | 0.0001 | 0.41 | 375 |
| AlCoCrFeNiMn_0.5 | SLM → Aged | 200°C | FCC | 4.2 | 8.6e14 | 654 | 876 | 328 | 22.6 | 0.001 | 0.25 | 586 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | rt | FCC | 12.5 |  | 268 | 523 | 178 | 51.3 | 0.0003 | 0.38 | 418 |
| AlCoCrNi | Cast → HIP | rt | FCC | 31.8 | 1.5e14 | 372 | 615 | 204 | 41.7 | 0.0001 | 0.35 |  |
| CoCrFeMnNi | SLM → Annealed | 400°C | FCC | 5.3 | 4.7e14 | 215 | 389 | 165 |  | 0.001 | 0.29 | 324 |
| AlFeNiTi_0.5 | Vacuum induction melted | rt | FCC | 24.1 | 2.8e14 | 438 | 686 | 245 | 27.9 | 0.0003 | 0.31 | 463 |
| CoCrCuFe | Arc-melted → Cold-rolled | 200°C | BCC + FCC | 7.8 | 7.2e14 | 526 | 782 |  | 18.3 | 0.001 | 0.22 | 615 |
| AlCoCrFe | SLM → HIP | rt | FCC | 9.2 | 5.6e14 | 492 | 751 | 243 | 25.7 |  | 0.28 | 528 |
| CrFeNiMn | Vacuum arc remelted | 400°C | FCC | 16.4 | 1.9e14 | 187 | 356 | 152 | 47.6 | 0.0003 | 0.42 | 298 |
| AlCuFeNi | Cast → Quenched | rt | L12 + FCC | 21.9 | 3.1e14 | 412 | 671 | 231 | 32.5 | 0.001 |  | 493 |
| CoCrFeMn | SLM → Stress-relieved | rt | FCC | 6.7 | 6.8e14 | 574 | 835 | 312 | 21.2 | 0.0001 | 0.24 | 642 |
| AlCoFeNi_0.7 | Arc-melted → Homogenized | 200°C | FCC | 19.2 | 2.5e14 | 342 | 597 | 197 |  | 0.0003 | 0.33 | 427 |
| CoCrCuFeMn | Induction melted → Hot-rolled | rt | FCC | 10.6 | 4.4e14 | 475 | 728 | 257 | 29.4 | 0.001 | 0.26 | 541 |
| AlCrFeMn | SLM → Aged | 400°C | BCC + FCC | 3.8 |  | 689 | 912 | 357 | 15.7 | 0.0003 | 0.19 | 695 |
| CoFeNiTi_0.3 | Cast → Annealed | rt | FCC | 28.4 | 1.7e14 | 295 | 547 | 189 | 43.8 | 0.0001 | 0.37 | 386 |
| AlCoCuFeNi | Arc-melted → Cold-rolled | rt | L12 + FCC |  | 6.3e14 | 631 | 864 | 342 | 16.9 | 0.001 | 0.21 | 672 |
| CrFeNiTi | SLM → HIP | 200°C | FCC | 5.7 | 7.9e14 | 587 | 842 | 307 | 19.5 | 0.0003 |  | 623 |
| AlCoMnNi | Vacuum induction melted | rt | FCC | 22.7 | 2.6e14 | 364 | 618 | 212 | 35.1 | 0.001 | 0.30 | 452 |
| CoCrFeCuNi | Arc-melted → Hot-rolled | 400°C | FCC | 13.9 | 2.1e14 | 173 |  | 148 | 49.2 | 0.0001 | 0.44 | 271 |
| AlFeNiCu_0.5 | Cast → Homogenized | rt | BCC + FCC | 15.3 | 3.8e14 | 457 | 712 | 261 | 23.8 | 0.0003 | 0.29 | 519 |
| CoCrMnNi | SLM → Annealed | rt | FCC | 7.1 | 6.5e14 | 547 | 815 | 296 |  | 0.001 | 0.25 | 601 |
| AlCrFeNi | Vacuum arc remelted | 200°C | FCC | 20.8 | 2.4e14 | 326 | 583 | 203 | 34.7 | 0.0001 | 0.34 | 415 |
| CoCuFeNi | Arc-melted → Quenched | rt | FCC | 14.5 | 4.2e14 |  | 695 | 238 | 28.6 | 0.0003 | 0.27 | 508 |
| AlCoFeMnNi_0.3 | SLM → Stress-relieved | 400°C | L12 + FCC | 4.9 | 8.3e14 | 612 | 857 | 324 | 17.2 | 0.001 | 0.20 | 653 |
| CrFeNiCu | Cast → HIP | rt | FCC | 27.2 | 1.6e14 | 278 | 534 |  | 44.5 | 0.0003 | 0.39 | 371 |
| AlCoCrMn | Arc-melted → Homogenized | rt | BCC + FCC | 9.7 | 5.1e14 | 512 | 768 | 275 | 24.3 |  | 0.26 | 574 |
| CoCrFeNiCu | Induction melted → Hot-rolled | 200°C | FCC | 11.2 | 3.7e14 | 387 | 649 | 221 | 31.8 | 0.001 | 0.28 | 481 |
| AlFeMnNi | SLM → Aged | rt | FCC | 6.4 | 7.5e14 | 568 | 827 | 318 | 20.1 | 0.0003 | 0.23 |  |
| CoCrFeTi_0.2 | Cast → Annealed | 400°C | FCC | 26.7 | 1.8e14 | 198 | 372 | 159 | 46.4 | 0.0001 | 0.40 | 312 |
| AlCoCuNi | Arc-meltmelted → Cold-rolled | rt | L12 + FCC | 8.9 |  | 598 | 845 | 327 | 19.3 | 0.001 | 0.22 | 647 |
| CrFeMnNi | SLM → HIP | rt | FCC | 5.1 | 8.8e14 | 623 | 875 | 339 |  | 0.0003 | 0.20 | 682 |
| AlCoCrFeMn | Vacuum induction melted | 200°C | FCC | 18.3 | 2.9e14 | 354 | 612 | 209 | 33.7 | 0.0001 | 0.32 | 442 |
| CoFeNiTi_0.5 | Arc-melted → Hot-rolled | rt | FCC + L12 | 12.8 | 4.3e14 | 467 | 723 | 251 | 25.9 | 0.001 |  | 533 |
| AlCrFeCu | Cast → Homogenized | 400°C | BCC + FCC | 23.4 | 2.2e14 | 245 | 492 | 173 | 39.3 | 0.0003 | 0.36 | 365 |
| CoCrNiMn | SLM → Annealed | rt | FCC |  | 6.7e14 | 534 | 804 | 291 | 21.7 | 0.0001 | 0.24 | 612 |
| AlCoFeNi | Vacuum arc remelted | rt | FCC | 29.5 | 1.9e14 | 314 | 568 | 195 | 38.9 | 0.001 | 0.35 | 406 |
| CoCrCuMn | Arc-melted → Quenched | 200°C | FCC | 10.9 | 5.5e14 | 486 | 742 |  | 24.6 | 0.0003 | 0.26 | 557 |
| AlFeMnTi_0.4 | SLM → Stress-relieved | rt | BCC + FCC | 4.5 | 9.4e14 | 713 | 935 | 372 | 14.8 | 0.001 | 0.18 |  |
| CoCrFeNiMn_0.3 | Cast → HIP | 400°C | FCC | 17.5 | 2.7e14 | 232 | 475 | 168 |  | 0.0001 | 0.38 | 352 |
| AlCoCrCu | Arc-melted → Homogenized | rt | L12 + FCC | 9.3 | 5.9e14 | 548 | 812 | 303 | 20.5 | 0.0003 | 0.23 | 621 |
| CrFeNiCuMn | Induction melted → Hot-rolled | rt | FCC | 11.7 |  | 423 | 687 | 234 | 29.3 | 0.001 | 0.28 | 498 |
| AlCoNiTi_0.3 | SLM → Aged | 200°C | FCC | 6.2 | 7.7e14 | 579 | 839 | 321 | 18.7 |  | 0.21 | 643 |
| CoCrMnTi | Cast → Annealed | rt | FCC | 27.9 | 1.7e14 | 287 | 542 | 186 | 42.3 | 0.0001 | 0.37 | 378 |
| AlCrNiMn | Arc-melted → Cold-rolled | 400°C | BCC + FCC | 8.3 | 6.4e14 |  | 691 | 248 | 21.4 | 0.001 | 0.24 | 584 |
| CoCuFeMn | SLM → HIP | rt | FCC | 5.6 | 8.1e14 | 603 | 863 | 334 | 17.1 | 0.0003 | 0.21 | 667 |
| AlCoFeCu | Vacuum induction melted | rt | FCC | 19.5 | 2.6e14 | 348 | 607 | 207 |  | 0.0001 | 0.31 | 437 |
| CoCrFeNiTi_0.2 | Arc-melted → Hot-rolled | 200°C | FCC | 13.2 | 3.9e14 | 396 | 658 | 225 | 30.5 | 0.001 | 0.29 | 472 |
| AlCrMnNi | Cast → Homogenized | rt | L12 + FCC | 24.6 |  | 318 | 573 | 196 | 37.4 | 0.0003 | 0.34 | 412 |
| CoCrFeCu | SLM → Annealed | 400°C | FCC | 7.2 | 6.9e14 | 403 | 665 | 229 | 26.8 | 0.0001 |  | 524 |
| AlFeNiMn | Vacuum arc remelted | rt | BCC + FCC | 30.1 | 1.6e14 | 269 | 527 | 180 | 45.9 | 0.001 | 0.40 | 359 |
| CoCuNiTi_0.5 | Arc-melted → Quenched | rt | FCC | 10.3 | 5.3e14 | 518 |  | 289 | 22.9 | 0.0003 | 0.25 | 592 |
| AlCoCrNiTi_0.3 | SLM → Stress-relieved | 200°C | FCC + L12 | 4.7 | 9.1e14 | 675 | 907 | 354 | 15.3 | 0.001 | 0.19 | 704 |
| CrFeMnCu | Cast → HIP | rt | FCC | 28.3 | 1.8e14 | 256 | 512 | 176 | 44.7 |  | 0.39 | 368 |
| AlCoCuMn | Arc-melted → Homogenized | 400°C | BCC + FCC | 9.4 | 5.7e14 | 367 | 631 | 214 |  | 0.0003 | 0.28 | 468 |
| CoCrNiCu | Induction melted → Hot-rolled | rt | FCC | 11.4 | 4.6e14 | 452 | 716 | 245 | 27.3 | 0.001 | 0.26 | 537 |
| AlFeCuTi_0.4 | SLM → Aged | rt | L12 + FCC |  | 7.6e14 | 563 | 825 | 317 | 18.4 | 0.0003 | 0.22 | 638 |
| CoCrFeMnTi_0.2 | Cast → Annealed | 200°C | FCC | 25.9 | 2.0e14 | 305 | 559 | 192 | 40.1 | 0.0001 | 0.36 |  |
| AlCoFeNiCu | Arc-melted → Cold-rolled | rt | FCC | 8.7 | 6.2e14 | 543 | 808 | 298 | 20.8 | 0.001 | 0.23 | 617 |""")

# Convert the file to CSV
df = markdown_to_csv(input_file, output_file)

# Display the first few rows to verify
print("\nFirst 5 rows of the CSV data:")
print(df.head())


# In[461]:


#gemini
import pandas as pd
import re

def markdown_to_csv(input_file, output_file):
    # Read the markdown file with UTF-8 encoding
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the table part (skip the title)
    table_start = content.find('|')
    if table_start == -1:
        raise ValueError("No table found in the input file")
    
    table_content = content[table_start:]
    
    # Split by lines
    lines = table_content.strip().split('\n')
    
    # Extract headers (first line)
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]
    
    # Skip the separator line (second line)
    data_lines = lines[2:]
    
    # Parse data rows
    data = []
    for line in data_lines:
        if '|' in line:  # Ensure it's a table row
            # Split by | and remove empty first and last elements
            row_values = [cell.strip() for cell in line.split('|')[1:-1]]
            data.append(row_values)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Export to CSV with UTF-8 encoding
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Successfully converted to CSV: {output_file}")
    
    return df

# Example usage
input_file = "hea_data_ge.txt"  # Your input file with the markdown table
output_file = "hea_data_gemini4.csv"  # Output CSV file

# Save the table data to a text file first with UTF-8 encoding
with open(input_file, 'w', encoding='utf-8') as f:
    f.write(""" # High Entropy Alloys (HEAs) Synthetic Dataset
    

| Composition | Processing Condition | Test Temperature | Phase | Grain Size (µm) | Dislocation Density (m⁻²) | YS (MPa) | UTS (MPa) | Hardness (HV) | Elongation (%) | Strain Rate (s⁻¹) | Strain Hardening Exponent (n) | Strain Hardening Coefficient (k) |
|-------------|---------------------|------------------|-------|-----------------|---------------------------|----------|-----------|---------------|----------------|-------------------|-------------------------------|----------------------------------|
| AlCoCrFeNi | Arc-melted → Annealed | rt | FCC | 25.3 | 3.4e14 | 387 | 642 | 217 | 38.5 | 0.001 | 0.32 | 412 |
| CoCrFeNi | Cast → Homogenized | rt | FCC | 18.7 | 1.8e14 | 241 | 479 | 185 | 45.2 | 0.0001 | 0.41 | 375 |
| AlCoCrFeNiMn_0.5 | SLM → Aged | 200°C | FCC | 4.2 | 8.6e14 | 654 | 876 | | 22.6 | 0.001 | 0.25 | 586 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | rt | FCC | 12.5 | | 268 | 523 | 178 | 51.3 | 0.0003 | 0.38 | 418 |
| AlCoCrNi | Cast → Annealed | 400°C | FCC | 32.1 | 2.5e14 | 425 | 689 | 235 | 32.1 | | 0.30 | 450 |
| AlCoCrFeNiCu_0.3 | SLM → Annealed | rt | FCC | 6.8 | 9.2e14 | 589 | 795 | 295 | 18.9 | 0.0005 | 0.28 | 550 |
| CoCrFeNiTi_0.2 | Arc-melted → Quenched | 200°C | FCC | 21.4 | 4.1e14 | 312 | 587 | 202 | 48.7 | 0.0001 | | 400 |
| AlCoFeNi | Cast → Extruded | rt | FCC | 15.9 | 1.5e14 | 285 | 542 | 192 | 55.4 | 0.0003 | 0.40 | |
| AlCrFeNi | SLM → HIP | 600°C | FCC | 3.5 | 1.1e15 | 782 | 1050 | 380 | 15.2 | 0.001 | 0.22 | 680 |
| CoFeMnNi | Arc-melted → Cold-rolled | rt | FCC | 10.2 | 2.8e14 | 305 | | 198 | 58.2 | 0.0001 | 0.43 | 380 |
| AlCoCrFeNi | Arc-melted → Annealed | 100°C | FCC | | 3.8e14 | 402 | 665 | 225 | 40.1 | 0.0002 | 0.33 | 425 |
| CoCrFeNi | Cast → Homogenized | 300°C | FCC | 20.1 | 2.0e14 | 255 | 502 | 190 | 47.5 | 0.0001 | 0.42 | 385 |
| AlCoCrFeNiMn_0.5 | SLM → Aged | rt | FCC | 5.1 | 9.0e14 | 670 | 900 | 335 | 24.1 | 0.0008 | 0.26 | 600 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | 200°C | | 13.8 | 3.0e14 | 280 | 540 | 182 | 53.0 | 0.0002 | 0.39 | 425 |
| AlCoCrNi | Cast → Annealed | rt | FCC | 30.5 | 2.2e14 | 410 | 670 | 230 | 30.8 | 0.0001 | 0.29 | 440 |
| AlCoCrFeNiCu_0.3 | SLM → Annealed | 100°C | FCC | 7.5 | 9.5e14 | 605 | 810 | 300 | | 0.0004 | 0.27 | 560 |
| CoCrFeNiTi_0.2 | Arc-melted → Quenched | rt | FCC | 22.8 | 4.5e14 | 325 | 600 | 208 | 50.5 | 0.0001 | 0.36 | 410 |
| AlCoFeNi | | 200°C | FCC | 16.5 | 1.6e14 | 295 | 560 | 195 | 57.0 | 0.0002 | 0.41 | 400 |
| AlCrFeNi | SLM → HIP | rt | FCC | 4.0 | 1.2e15 | 800 | 1080 | 390 | 16.0 | 0.0009 | 0.23 | 700 |
| CoFeMnNi | Arc-melted → Cold-rolled | 100°C | FCC | 11.0 | 3.0e14 | 320 | 580 | | 60.0 | 0.0001 | 0.44 | 390 |
| AlCoCrFeNiMn | Arc-melted → Annealed | 400°C | FCC | 27 | 3.6e14 | 450 | 700 | 240 | 35 | 0.0005 | 0.31 | 440 |
| CoCrFeNi | Cast → Homogenized | rt | FCC | 19.5 | | 250 | 490 | 188 | 46 | 0.0002 | 0.40 | 380 |
| AlCoCrFeNiMn_0.5 | SLM → Aged | 200°C | FCC | 4.8 | 8.8e14 | 660 | 890 | 330 | 23.5 | 0.0007 | 0.255 | 590 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | rt | FCC | 13 | | 275 | 530 | 180 | 52 | 0.00025 | 0.385 | 420 |
| AlCoCrNi | Cast → Annealed | 400°C | FCC | 31.5 | 2.4e14 | 420 | | 233 | 31.5 | 0.00015 | 0.295 | 445 |
| AlCoCrFeNiCu_0.3 | SLM → Annealed | rt | FCC | 7.2 | 9.35e14 | 595 | 800 | 298 | 19.5 | 0.00045 | 0.275 | 555 |
| CoCrFeNiTi_0.2 | Arc-melted → Quenched | 200°C | FCC | 22 | 4.3e14 | | 595 | 205 | 49.5 | 0.00012 | 0.355 | 405 |
| AlCoFeNi | Cast → Extruded | rt | FCC | 16.2 | 1.55e14 | 290 | 550 | 193.5 | 56.2 | 0.00028 | 0.405 | 395 |
| AlCrFeNi | SLM → HIP | 600°C | FCC | 3.75 | 1.15e15 | 790 | 1065 | 385 | 15.6 | 0.00095 | | 690 |
| CoFeMnNi | Arc-melted → Cold-rolled | rt | FCC | 10.6 | 2.9e14 | 310 | 570 | 201.5 | 59.1 | 0.00011 | 0.435 | 385 |
| AlCoCrFeNi | Arc-melted → Annnealed | 150°C | FCC | 26.5 | 3.55e14 | 395 | 650 | 220 | 39.3 | | 0.325 | 418 |
| CoCrFeNi | Cast → Homogenized | 350°C | FCC | 19.85 | 1.95e14 | 252.5 | 496 | 189 | 46.75 | 0.000125 | 0.415 | 382.5 |
| AlCoCrFeNiMn_0.5 | SLM → Aged | rt | FCC | 4.95 | 8.9e14 | 665 | 895 | 332.5 | 23.8 | 0.00075 | 0.2525 | |
| CoCrFeNiMn | Arc-melted → Hot-rolled | 250°C | FCC | 13.4 | 2.95e14 | 277.5 | 535 | 181 | 52.5 | 0.000275 | 0.3875 | 422.5 |
| AlCoCrNi | Cast → Annealed | rt | FCC | 31 | 2.3e14 | 415 | 675 | 231.5 | | 0.00013 | 0.2925 | 442.5 |
| AlCoCrFeNiCu_0.3 | SLM → Annealed | 150°C | FCC | 7.35 | | 600 | 805 | 299 | 19.85 | 0.000475 | 0.2725 | 557.5 |
| CoCrFeNiTi_0.2 | Arc-melted → Quenched | rt | FCC | 22.4 | 4.4e14 | 322.5 | 597.5 | 206.5 | 50 | 0.000115 | 0.3575 | 407.5 |
| AlCoFeNi | Cast → Extruded | 250°C | FCC | | 1.575e14 | 292.5 | 555 | 194.25 | 56.6 | 0.000265 | 0.4075 | 397.5 |
| AlCrFeNi | SLM → HIP | rt | FCC | 3.9 | 1.175e15 | 795 | 1072.5 | 387.5 | 15.8 | 0.000975 | 0.2275 | 695 |
| CoFeMnNi | Arc-melted → Cold-rolled | 150°C | FCC | 10.8 | 2.95e14 | 315 | 575 | 203.25 | 59.55 | | 0.4375 | 387.5 |
| AlCoCrFeNiTi_0.1 | Arc-melted → Annealed | 300°C | FCC | 24.5 | 3.3e14 | 420 | 680 | | 36 | 0.0004 | 0.315 | 430 |
| CoCrFeNiMo_0.1 | Cast → Homogenized | rt | FCC | 17.9 | 1.7e14 | 260 | 510 | 195 | 44 | 0.00015 | 0.405 | 390 |
| AlCoCrFeNiV_0.1 | SLM → Aged | 400°C | FCC | 6.2 | 8.2e14 | 700 | | 350 | 20 | 0.0009 | 0.24 | 620 |
| CoCrFeMnNi | Arc-melted → Hot-rolled | 100°C | FCC | 11.8 | | 290 | 550 | 190 | 50 | 0.00028 | 0.375 | 430 |
| AlCoCrNiCu_0.2 | Cast → Annealed | rt | FCC | 29.2 | 2.1e14 | 400 | 650 | 225 | 28 | 0.00012 | | 435 |
| AlCoCrFeNi | SLM → Annealed | 200°C | FCC | 8.1 | 9.8e14 | 620 | 830 | 310 | 17 | 0.00055 | 0.265 | 570 |
| CoCrFeNiTi_0.3 | Arc-melted → Quenched | rt | FCC | 20.7 | 4.0e14 | 330 | 610 | 210 | 47 | | 0.345 | 415 |
| AlCoFeNiMn_0.1 | Cast → Extruded | 300°C | FCC | 14.5 | 1.4e14 | 300 | 570 | 200 | 53 | 0.00022 | 0.395 | 405 |
| AlCrFeNiMn_0.1 | SLM → HIP | rt | FCC | 5.5 | 1.05e15 | 750 | 1000 | 360 | 14 | 0.00085 | 0.215 | |
| CoFeMnNiCr_0.1 | Arc-melted → Cold-rolled | 200°C | FCC | 9.8 | 2.7e14 | 325 | 590 | 208 | | 0.000115 | 0.425 | 395 |
| AlCoCrFeNi | Arc-melted → Annealed | rt | FCC | 27.8 | 3.7e14 | 410 | 670 | 228 | 41 | 0.00035 | 0.335 | 430 |
| CoCrFeNi | Cast → Homogenized | 250°C | | 19.2 | 1.9e14 | 248 | 485 | 187 | 48 | 0.00014 | 0.418 | 388 |
| AlCoCrFeNiMn_0.4 | SLM → Aged | 100°C | FCC | 5.3 | 9.1e14 | 680 | 910 | 340 | 25 | 0.00065 | 0.258 | 605 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | 300°C | FCC | 14.1 | 3.1e14 | | 545 | 185 | 54 | 0.00029 | 0.392 | 428 |
| AlCoCrNi | Cast → Annealed | rt | FCC | 32.5 | 2.35e14 | 430 | 690 | 238 | 32 | 0.000145 | 0.298 | 450 |
| AlCoCrFeNiCu_0.2 | SLM → Annealed | 200°C | FCC | 7.85 | | 610 | 820 | 305 | 21 | 0.000525 | 0.278 | 565 |
| CoCrFeNiTi_0.3 | Arc-melted → Quenched | rt | FCC | 21.7 | 4.2e14 | 327 | 605 | 207.5 | 51 | 0.000125 | 0.353 | 412.5 |
| AlCoFeNi | Cast → Extruded | 250°C | FCC | 16 | 1.525e14 | 297 | 565 | | 57.5 | 0.000245 | 0.403 | 398.5 |
| AlCrFeNi | SLM → HIP | 500°C | FCC | 4.25 | 1.2e15 | 775 | 1040 | 375 | 17.5 | 0.000925 | 0.223 | 685 |
| CoFeMnNi | Arc-melted → Cold-rolled | 250°C | FCC | 11.3 | 3.05e14 | 322 | 585 | 206 | 60.5 | 0.00011 | | 392.5 |
| AlCoCrFeNi | Arc-melted → Annealed | rt | FCC | 26 | | 400 | 660 | 222 | 39 | 0.0003 | 0.328 | 420 |
| CoCrFeNi | Cast → Homogenized | 300°C | FCC | 18.2 | 1.8e14 | 245 | 480 | 184 | 46.5 | 0.00013 | 0.413 | 380 |
| AlCoCrFeNiMn_0.4 | SLM → Aged | 200°C | FCC | 5.15 | 8.95e14 | 670 | 900 | 335 | | 0.0007 | 0.2555 | 595 |
| CoCrFeNiMn | Arc-melted → Hot-rolled | rt | FCC | 13.7 | | 280 | 540 | 183 | 53.5 | 0.000265 | 0.3885 | 425 |
| AlCoCrNi | Cast → Annealed | 400°C | FCC | 31.8 | 2.325e14 | 425 | 685 | 235.5 | 31.85 | 0.000145 | | 447.5 |
| AlCoCrFeNiCu_0.2 | SLM → Annealed | rt | FCC | 7.6 | 9.525e14 | 605 | 810 | 302.5 | 20.5 | 0.00049 | 0.2755 | 560 |
| CoCrFeNiTi_0.3 | Arc-melted → Quenched | 200°C | FCC | | 4.325e14 | 328.5 | 607.5 | 208.75 | 50.25 | 0.000128 | 0.3555 | 410.5 |
| AlCoFeNi | Cast → Extruded | rt | FCC | 16.1 | 1.54e14 | 294.5 | 560 | 194 | 57.15 | 0.000275 | 0.4055 | |
| AlCrFeNi | SLM → HIP | 600°C | FCC | 3.85 | 1.16e15 | 792.5 | 1070 | 386.25 | 15.7 | | 0.2265 | 692.5 |
| CoFeMnNi | Arc-melted → Cold-rolled | rt | FCC | 10.75 | 2.925e14 | 312.5 | 572.5 | 202.4 | 59.3 | 0.000108 | 0.4365 | 386.5 |


""")
# Convert the file to CSV
df = markdown_to_csv(input_file, output_file)

# Display the first few rows to verify
print("\nFirst 5 rows of the CSV data:")
print(df.head())


# In[462]:


#perplexity
import pandas as pd
import random

# Helper functions for realistic data generation
def random_composition():
    elements = ["Al", "Co", "Cr", "Fe", "Ni", "Mn", "Cu", "Ti"]
    return "-".join(random.sample(elements, random.randint(3,5)))

def realistic_value(range, decimals=2):
    return round(random.uniform(*range), decimals) if random.random() > 0.1 else None

# Generate 60 entries
data = {
    "Composition": [random_composition() for _ in range(60)],
    "Processing Condition": [random.choice(["Arc-melted → Annealed", "SLM → Aged"]) if random.random() > 0.1 else None for _ in range(60)],
    "Test Temperature (°C)": [random.choice(["rt", 200, 400]) if random.random() > 0.1 else None for _ in range(60)],
    "Phase": [random.choice(["FCC", "FCC + BCC", "L12 + FCC"]) if random.random() > 0.1 else None for _ in range(60)],
    "Grain Size (µm)": [realistic_value((0.1, 100)) for _ in range(60)],
    "Dislocation Density (dislocations/m²)": [realistic_value((1e12, 1e15)) for _ in range(60)],
    "Yield Strength (MPa)": [realistic_value((100, 1000)) for _ in range(60)],
    "UTS (MPa)": [realistic_value((200, 1500)) for _ in range(60)],
    "Hardness (HV)": [realistic_value((50, 500)) for _ in range(60)],
    "Elongation (%)": [realistic_value((1, 50)) for _ in range(60)],
    "Strain Rate (s⁻¹)": [realistic_value((1e-5, 1e-1)) for _ in range(60)],
    "Strain Hardening Exponent (n)": [realistic_value((0.1, 0.5)) for _ in range(60)],
    "Strain Hardening Coefficient (k)": [realistic_value((100, 1000)) for _ in range(60)]
}

df = pd.DataFrame(data)
df.to_csv("hea_data_perplexity.csv",index=False)
df.head(60)


# ### DATA ANALYSIS

# In[463]:


df_chatgpt = pd.read_csv('hea_data_chatgpt.csv')
df_claude = pd.read_csv('hea_data_claude.csv')
df_gemini = pd.read_csv('hea_data_gemini4.csv')
df_perplex = pd.read_csv('hea_data_perplexity.csv')


# In[464]:


df_chatgpt.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_chatgpt.rename(columns={'Composition': 'Alloy'}, inplace=True)
df_claude.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_claude.rename(columns={'Composition': 'Alloy'}, inplace=True)
df_gemini.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_gemini.rename(columns={'Composition': 'Alloy'}, inplace=True)
df_perplex.rename(columns={'Composition': 'Alloy'}, inplace=True)
df_perplex.rename(columns={'Test Temperature (°C) ': 'Test Temperature (°C)'}, inplace=True)


# In[465]:


df_chatgpt.columns


# #### CHATGPT DATASETS

# In[466]:


import pandas as pd

df_chatgpt = pd.read_csv('hea_data_chatgpt.csv')


# In[467]:


df_chatgpt.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_chatgpt.rename(columns={'Composition': 'Alloy'}, inplace=True)


# In[468]:


df_chatgpt.head()


# In[469]:


df_chatgpt.columns


# In[470]:


df_chatgpt["Test Temperature"] = df_chatgpt["Test Temperature"].replace("RT", "25°C")
df_chatgpt["Test Temperature (°C)"] = df_chatgpt["Test Temperature"].str.extract(r'(\d+\.?\d*)').astype(float)


# In[471]:


df_chatgpt


# In[472]:


df_chatgpt = df_chatgpt.drop(columns=["Test Temperature"])
df_chatgpt.isnull().sum()


# In[473]:


df_chatgpt['Processing Condition'].fillna(df_chatgpt['Hardness (HV)'].mode(), inplace=True)
df_chatgpt['Hardness (HV)'].fillna(df_chatgpt['Hardness (HV)'].median(), inplace=True)
df_chatgpt['Elongation (%)'] = df_chatgpt['Elongation (%)'].fillna(df_chatgpt['Elongation (%)'].median())


# In[474]:


df_chatgpt.isnull().sum()


# In[475]:


df_chatgpt.describe()


# In[476]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[477]:


#Histograms for Distribution
df_chatgpt.hist(figsize=(15, 10), bins=15, edgecolor='black')
plt.suptitle("Histograms of Numeric Features")
plt.tight_layout()
plt.show()


# In[478]:


#Box Plots for Outliers
plt.figure(figsize=(16, 6))
sns.boxplot(data=df_chatgpt.select_dtypes(include='number'))
plt.xticks(rotation=45)
plt.title("Box Plot of Numeric Columns")
plt.show()


# In[479]:


# Correlation Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df_chatgpt.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()


# In[480]:


# Pair Plot (Scatter Matrix)
sns.pairplot(df_chatgpt.dropna(), corner=True)
plt.suptitle("Pairplot of Numerical Variables", y=1.02)
plt.show()


# In[481]:


df_chatgpt.columns


# In[482]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define all x-y pairs with their interpretation
plot_pairs = [
    ("Grain Size (µm)", "Yield Strength (MPa)", "YS vs Grain Size (colored by Phase)"),
    ("Grain Size (µm)", "UTS (MPa)", "UTS vs Grain Size (colored by Phase)"),
    ("Hardness (HV)", "Yield Strength (MPa)", "YS vs Hardness (colored by Phase)"),
    ("Hardness (HV)", "UTS (MPa)", "UTS vs Hardness (colored by Phase)"),
    ("Dislocation Density (dislocations/m²)", "Yield Strength (MPa)", "YS vs Dislocation Density (colored by Phase)"),
    ("Strain Rate (s⁻¹)", "Elongation (%)", "Elongation vs Strain Rate (colored by Phase)"),
    ("Strain Hardening Exponent (n)", "Strain Hardening Coefficient (k)", "n vs k (colored by Phase)"),
    ("Grain Size (µm)", "Hardness (HV)", "Hardness vs Grain Size (colored by Phase)"),
    ("Yield Strength (MPa)", "Elongation (%)", "Elongation vs YS (colored by Phase)")
]

# Create scatter plots
plt.figure(figsize=(18, 24))  # Adjust height for all subplots
for i, (x, y, title) in enumerate(plot_pairs):
    plt.subplot(3, 3, i+1)
    sns.scatterplot(data=df_chatgpt, x=x, y=y, hue="Phase")
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()

plt.suptitle("Scatter Plots of Key Mechanical Relationships (colored by Phase)", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# In[483]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define the category-numeric axis pairs and their titles
violin_pairs = [
    ("Phase", "Hardness (HV)", "Hardness Distribution by Phase"),
    ("Phase", "Yield Strength (MPa)", "Yield Strength Distribution by Phase"),
    ("Phase", "UTS (MPa)", "UTS Distribution by Phase"),
    ("Phase", "Grain Size (µm)", "Grain Size Distribution by Phase"),
    ("Phase", "Elongation (%)", "Elongation Distribution by Phase"),
    ("Phase", "Dislocation Density (dislocations/m²)", "Dislocation Density by Phase"),
    ("Phase", "Strain Rate (s⁻¹)", "Strain Rate Distribution by Phase"),
    ("Phase", "Strain Hardening Exponent (n)", "n (Hardening Exponent) by Phase"),
    ("Phase", "Strain Hardening Coefficient (k)", "k (Hardening Coefficient) by Phase"),
    ("Processing Condition", "Hardness (HV)", "Hardness vs Processing Condition"),
    ("Processing Condition", "Yield Strength (MPa)", "Yield Strength vs Processing Condition"),
    ("Test Temperature (°C)", "Elongation (%)", "Elongation vs Test Temperature"),
]

# Set up the figure
plt.figure(figsize=(20, 20))
for i, (x, y, title) in enumerate(violin_pairs):
    plt.subplot(4, 3, i + 1)
    sns.violinplot(data=df_chatgpt, x=x, y=y, color='pink', alpha=0.6)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=9)
    plt.ylabel(y, fontsize=9)
    plt.xticks(rotation=45)

plt.suptitle("Violin Plots Showing Distribution of Mechanical Properties Across Categories", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()



# In[484]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of columns for Boxplot with their interpretations
boxplot_columns = [
    ("Elongation (%)", "Phase", "Elongation Distribution by Phase"),
    ("Yield Strength (MPa)", "Phase", "YS Distribution by Phase"),
    ("UTS (MPa)", "Phase", "UTS Distribution by Phase"),
    ("Hardness (HV)", "Phase", "Hardness Distribution by Phase"),
    ("Grain Size (µm)", "Phase", "Grain Size Distribution by Phase"),
    ("Dislocation Density (dislocations/m²)", "Phase", "Dislocation Density Distribution by Phase"),
    ("Strain Rate (s⁻¹)", "Phase", "Strain Rate Distribution by Phase"),
    ("Strain Hardening Exponent (n)", "Phase", "Strain Hardening Exponent Distribution by Phase"),
    ("Strain Hardening Coefficient (k)", "Phase", "Strain Hardening Coefficient Distribution by Phase")
]

# Create boxplots
plt.figure(figsize=(16, 18))  # Adjusting figure size for all subplots
for i, (y, x, title) in enumerate(boxplot_columns):
    plt.subplot(3, 3, i+1)
    sns.boxplot(data=df_chatgpt, x=x, y=y)
    plt.xticks(rotation=45)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.tight_layout()

plt.suptitle("Box Plots for Key Mechanical Properties by Phase", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# ### CLAUDE

# In[485]:


import pandas as pd

df_claude = pd.read_csv('hea_data_claude.csv')
df_claude.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_claude.rename(columns={'Composition': 'Alloy'}, inplace=True)
df_claude.head()


# In[486]:


df_claude.columns


# In[487]:


df_claude["Test Temperature"] = df_claude["Test Temperature"].replace("RT", "25°C")
df_claude["Test Temperature (°C)"] = df_claude["Test Temperature"].str.extract(r'(\d+\.?\d*)').astype(float)


# In[488]:


df_claude.columns


# In[489]:


df_claude = df_claude.drop(columns=['Test Temperature'])
df_claude.isnull().sum()


# In[490]:


numeric_cols = [
    'Grain Size (µm)', 'Dislocation Density (m⁻²)', 'Yield Strength (MPa)', 'UTS (MPa)',
    'Hardness (HV)', 'Elongation (%)', 'Strain Rate (s⁻¹)',
    'Strain Hardening Exponent (n)', 'Strain Hardening Coefficient (k)', 'Test Temperature (°C)'
]

# Convert all to numeric (coerce errors if any string is present)
df_claude[numeric_cols] = df_claude[numeric_cols].apply(pd.to_numeric, errors='coerce')


# In[491]:


# Fill numerical columns with mean
num_cols = [
    'Grain Size (µm)', 'Dislocation Density (m⁻²)', 'Yield Strength (MPa)', 
    'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)', 'Strain Rate (s⁻¹)', 
    'Strain Hardening Exponent (n)', 'Strain Hardening Coefficient (k)', 'Test Temperature (°C)'
]
df_claude[num_cols] = df_claude[num_cols].apply(lambda col: col.fillna(col.mean()))

# Fill categorical columns with mode
cat_cols = ['Processing Condition', 'Phase']
df_claude[cat_cols] = df_claude[cat_cols].apply(lambda col: col.fillna(col.mode()[0]))


# In[492]:


df_claude.isnull().sum()


# In[493]:


df_claude.describe()


# In[494]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[495]:


#Histograms for Distribution
df_claude.hist(figsize=(15, 10), bins=15, edgecolor='black')
plt.suptitle("Histograms of Numeric Features")
plt.tight_layout()
plt.show()


# In[496]:


#Box Plots for Outliers
plt.figure(figsize=(16, 6))
sns.boxplot(data=df_claude.select_dtypes(include='number'))
plt.xticks(rotation=45)
plt.title("Box Plot of Numeric Columns")
plt.show()


# In[497]:


plt.figure(figsize=(10, 8))
sns.heatmap(df_claude.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()


# In[498]:


# Pair Plot (Scatter Matrix)
sns.pairplot(df_claude.dropna(), corner=True)
plt.suptitle("Pairplot of Numerical Variables", y=1.02)
plt.show()


# In[499]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define all x-y pairs with their interpretation
plot_pairs = [
    ("Grain Size (µm)", "Yield Strength (MPa)", "YS vs Grain Size (colored by Phase)"),
    ("Grain Size (µm)", "UTS (MPa)", "UTS vs Grain Size (colored by Phase)"),
    ("Hardness (HV)", "Yield Strength (MPa)", "YS vs Hardness (colored by Phase)"),
    ("Hardness (HV)", "UTS (MPa)", "UTS vs Hardness (colored by Phase)"),
    ("Dislocation Density (m⁻²)", "Yield Strength (MPa)", "YS vs Dislocation Density (colored by Phase)"),
    ("Strain Rate (s⁻¹)", "Elongation (%)", "Elongation vs Strain Rate (colored by Phase)"),
    ("Strain Hardening Exponent (n)", "Strain Hardening Coefficient (k)", "n vs k (colored by Phase)"),
    ("Grain Size (µm)", "Hardness (HV)", "Hardness vs Grain Size (colored by Phase)"),
    ("Yield Strength (MPa)", "Elongation (%)", "Elongation vs YS (colored by Phase)")
]

# Create scatter plots
plt.figure(figsize=(18, 24))  # Adjust height for all subplots
for i, (x, y, title) in enumerate(plot_pairs):
    plt.subplot(3, 3, i+1)
    sns.scatterplot(data=df_claude, x=x, y=y, hue="Phase")
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()

plt.suptitle("Scatter Plots of Key Mechanical Relationships (colored by Phase)", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# In[500]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define the category-numeric axis pairs and their titles
violin_pairs = [
    ("Phase", "Hardness (HV)", "Hardness Distribution by Phase"),
    ("Phase", "Yield Strength (MPa)", "Yield Strength Distribution by Phase"),
    ("Phase", "UTS (MPa)", "UTS Distribution by Phase"),
    ("Phase", "Grain Size (µm)", "Grain Size Distribution by Phase"),
    ("Phase", "Elongation (%)", "Elongation Distribution by Phase"),
    ("Phase", "Dislocation Density (m⁻²)", "Dislocation Density by Phase"),
    ("Phase", "Strain Rate (s⁻¹)", "Strain Rate Distribution by Phase"),
    ("Phase", "Strain Hardening Exponent (n)", "n (Hardening Exponent) by Phase"),
    ("Phase", "Strain Hardening Coefficient (k)", "k (Hardening Coefficient) by Phase"),
    ("Processing Condition", "Hardness (HV)", "Hardness vs Processing Condition"),
    ("Processing Condition", "Yield Strength (MPa)", "Yield Strength vs Processing Condition"),
    ("Test Temperature (°C)", "Elongation (%)", "Elongation vs Test Temperature"),
]

# Set up the figure
plt.figure(figsize=(20, 20))
for i, (x, y, title) in enumerate(violin_pairs):
    plt.subplot(4, 3, i + 1)
    sns.violinplot(data=df_claude, x=x, y=y, color='pink', alpha=0.6)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=9)
    plt.ylabel(y, fontsize=9)
    plt.xticks(rotation=45)

plt.suptitle("Violin Plots Showing Distribution of Mechanical Properties Across Categories", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()



# In[501]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of columns for Boxplot with their interpretations
boxplot_columns = [
    ("Elongation (%)", "Phase", "Elongation Distribution by Phase"),
    ("Yield Strength (MPa)", "Phase", "YS Distribution by Phase"),
    ("UTS (MPa)", "Phase", "UTS Distribution by Phase"),
    ("Hardness (HV)", "Phase", "Hardness Distribution by Phase"),
    ("Grain Size (µm)", "Phase", "Grain Size Distribution by Phase"),
    ("Dislocation Density (m⁻²)", "Phase", "Dislocation Density Distribution by Phase"),
    ("Strain Rate (s⁻¹)", "Phase", "Strain Rate Distribution by Phase"),
    ("Strain Hardening Exponent (n)", "Phase", "Strain Hardening Exponent Distribution by Phase"),
    ("Strain Hardening Coefficient (k)", "Phase", "Strain Hardening Coefficient Distribution by Phase")
]

# Create boxplots
plt.figure(figsize=(16, 18))  # Adjusting figure size for all subplots
for i, (y, x, title) in enumerate(boxplot_columns):
    plt.subplot(3, 3, i+1)
    sns.boxplot(data=df_claude, x=x, y=y)
    plt.xticks(rotation=45)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.tight_layout()

plt.suptitle("Box Plots for Key Mechanical Properties by Phase", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# #### GEMINI

# In[502]:


import pandas as pd

df_gemini = pd.read_csv('hea_data_gemini4.csv')
df_gemini.rename(columns={'YS (MPa)': 'Yield Strength (MPa)'}, inplace=True)
df_gemini.rename(columns={'Composition': 'Alloy'}, inplace=True)

df_gemini.head()


# In[503]:


df_gemini.columns


# In[504]:


df_gemini["Test Temperature"] = df_gemini["Test Temperature"].replace("RT", "25°C")
df_gemini["Test Temperature (°C)"] = df_gemini["Test Temperature"].str.extract(r'(\d+\.?\d*)').astype(float)


# In[505]:


df_gemini = df_gemini.drop(columns=["Test Temperature"])
df_gemini.isnull().sum()


# In[506]:


df_gemini['Test Temperature (°C)'].fillna(25, inplace=True)


# In[507]:


numeric_cols = [
    'Grain Size (µm)', 'Dislocation Density (m⁻²)', 'Yield Strength (MPa)', 'UTS (MPa)',
    'Hardness (HV)', 'Elongation (%)', 'Strain Rate (s⁻¹)',
    'Strain Hardening Exponent (n)', 'Strain Hardening Coefficient (k)', 'Test Temperature (°C)'
]

# Convert all to numeric (coerce errors if any string is present)
df_gemini[numeric_cols] = df_gemini[numeric_cols].apply(pd.to_numeric, errors='coerce')


# In[508]:


# Fill numerical columns with mean
num_cols = [
    'Grain Size (µm)', 'Dislocation Density (m⁻²)', 'Yield Strength (MPa)', 
    'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)', 'Strain Rate (s⁻¹)', 
    'Strain Hardening Exponent (n)', 'Strain Hardening Coefficient (k)', 'Test Temperature (°C)'
]
df_gemini[num_cols] = df_gemini[num_cols].apply(lambda col: col.fillna(col.mean()))

# Fill categorical columns with mode
cat_cols = ['Processing Condition', 'Phase']
df_gemini[cat_cols] = df_gemini[cat_cols].apply(lambda col: col.fillna(col.mode()[0]))


# In[509]:


df_gemini.isnull().sum()


# In[510]:


df_gemini.describe()


# In[511]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[512]:


#Histograms for Distribution
df_gemini.hist(figsize=(15, 10), bins=15, edgecolor='black')
plt.suptitle("Histograms of Numeric Features")
plt.tight_layout()
plt.show()


# In[513]:


#Box Plots for Outliers
plt.figure(figsize=(16, 6))
sns.boxplot(data=df_gemini.select_dtypes(include='number'))
plt.xticks(rotation=45)
plt.title("Box Plot of Numeric Columns")
plt.show()


# In[514]:


plt.figure(figsize=(10, 8))
sns.heatmap(df_gemini.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()


# In[515]:


# Pair Plot (Scatter Matrix)
sns.pairplot(df_gemini.dropna(), corner=True)
plt.suptitle("Pairplot of Numerical Variables", y=1.02)
plt.show()


# In[516]:


df_gemini.columns


# In[517]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define all x-y pairs with their interpretation
plot_pairs = [
    ("Grain Size (µm)", "Yield Strength (MPa)", "YS vs Grain Size (colored by Phase)"),
    ("Grain Size (µm)", "UTS (MPa)", "UTS vs Grain Size (colored by Phase)"),
    ("Hardness (HV)", "Yield Strength (MPa)", "YS vs Hardness (colored by Phase)"),
    ("Hardness (HV)", "UTS (MPa)", "UTS vs Hardness (colored by Phase)"),
    ("Dislocation Density (m⁻²)", "Yield Strength (MPa)", "YS vs Dislocation Density (colored by Phase)"),
    ("Strain Rate (s⁻¹)", "Elongation (%)", "Elongation vs Strain Rate (colored by Phase)"),
    ("Strain Hardening Exponent (n)", "Strain Hardening Coefficient (k)", "n vs k (colored by Phase)"),
    ("Grain Size (µm)", "Hardness (HV)", "Hardness vs Grain Size (colored by Phase)"),
    ("Yield Strength (MPa)", "Elongation (%)", "Elongation vs YS (colored by Phase)")
]

# Create scatter plots
plt.figure(figsize=(18, 24))  # Adjust height for all subplots
for i, (x, y, title) in enumerate(plot_pairs):
    plt.subplot(3, 3, i+1)
    sns.scatterplot(data=df_gemini, x=x, y=y, hue="Phase")
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()

plt.suptitle("Scatter Plots of Key Mechanical Relationships (colored by Phase)", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# In[518]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define the category-numeric axis pairs and their titles
violin_pairs = [
    ("Phase", "Hardness (HV)", "Hardness Distribution by Phase"),
    ("Phase", "Yield Strength (MPa)", "Yield Strength Distribution by Phase"),
    ("Phase", "UTS (MPa)", "UTS Distribution by Phase"),
    ("Phase", "Grain Size (µm)", "Grain Size Distribution by Phase"),
    ("Phase", "Elongation (%)", "Elongation Distribution by Phase"),
    ("Phase", "Dislocation Density (m⁻²)", "Dislocation Density by Phase"),
    ("Phase", "Strain Rate (s⁻¹)", "Strain Rate Distribution by Phase"),
    ("Phase", "Strain Hardening Exponent (n)", "n (Hardening Exponent) by Phase"),
    ("Phase", "Strain Hardening Coefficient (k)", "k (Hardening Coefficient) by Phase"),
    ("Processing Condition", "Hardness (HV)", "Hardness vs Processing Condition"),
    ("Processing Condition", "Yield Strength (MPa)", "Yield Strength vs Processing Condition"),
    ("Test Temperature (°C)", "Elongation (%)", "Elongation vs Test Temperature"),
]

# Set up the figure
plt.figure(figsize=(20, 20))
for i, (x, y, title) in enumerate(violin_pairs):
    plt.subplot(4, 3, i + 1)
    sns.violinplot(data=df_gemini, x=x, y=y, color='pink', alpha=0.6)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=9)
    plt.ylabel(y, fontsize=9)
    plt.xticks(rotation=45)

plt.suptitle("Violin Plots Showing Distribution of Mechanical Properties Across Categories", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()



# In[519]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of columns for Boxplot with their interpretations
boxplot_columns = [
    ("Elongation (%)", "Phase", "Elongation Distribution by Phase"),
    ("Yield Strength (MPa)", "Phase", "YS Distribution by Phase"),
    ("UTS (MPa)", "Phase", "UTS Distribution by Phase"),
    ("Hardness (HV)", "Phase", "Hardness Distribution by Phase"),
    ("Grain Size (µm)", "Phase", "Grain Size Distribution by Phase"),
    ("Dislocation Density (m⁻²)", "Phase", "Dislocation Density Distribution by Phase"),
    ("Strain Rate (s⁻¹)", "Phase", "Strain Rate Distribution by Phase"),
    ("Strain Hardening Exponent (n)", "Phase", "Strain Hardening Exponent Distribution by Phase"),
    ("Strain Hardening Coefficient (k)", "Phase", "Strain Hardening Coefficient Distribution by Phase")
]

# Create boxplots
plt.figure(figsize=(16, 18))  # Adjusting figure size for all subplots
for i, (y, x, title) in enumerate(boxplot_columns):
    plt.subplot(3, 3, i+1)
    sns.boxplot(data=df_gemini, x=x, y=y)
    plt.xticks(rotation=45)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.tight_layout()

plt.suptitle("Box Plots for Key Mechanical Properties by Phase", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# In[ ]:





# #### PERPLEXITY

# In[520]:


import pandas as pd

df_perplex = pd.read_csv('hea_data_perplexity.csv')
df_perplex.rename(columns={'Composition': 'Alloy'}, inplace=True)
#df_perplex.rename(columns={'Test Temperature (°C) ': 'Test Temperature (°C)'}, inplace=True)
df_perplex.head()


# In[521]:


df_perplex.columns


# In[522]:


df_perplex["Test Temperature (°C)"] = df_perplex["Test Temperature (°C)"].replace("RT", "25°C")
df_perplex["Test Temperature (°C)"] = df_perplex["Test Temperature (°C)"].str.extract(r'(\d+\.?\d*)').astype(float)


# In[523]:


df_perplex.columns


# In[524]:


df_perplex = df_perplex.drop(columns=["Test Temperature (°C)"])
df_perplex.isnull().sum()


# In[525]:


# 1. Fill Categorical Columns with Mode
df_perplex['Processing Condition'].fillna(df_perplex['Processing Condition'].mode()[0], inplace=True)
df_perplex['Phase'].fillna(df_perplex['Phase'].mode()[0], inplace=True)

# 2. Fill Numeric Columns with Mean
num_cols = [
    'Grain Size (µm)',  'Dislocation Density (dislocations/m²)','Yield Strength (MPa)', 'UTS (MPa)', 'Hardness (HV)', 
    'Elongation (%)','Strain Rate (s⁻¹)', 'Strain Hardening Exponent (n)', 
    'Strain Hardening Coefficient (k)'
]

df_perplex[num_cols] = df_perplex[num_cols].apply(lambda col: col.fillna(col.mean()))

#df_perplex['Test Temperature (°C)'].fillna(25, inplace=True)
if 'Test Temperature (°C)' not in df_perplex.columns:
    df_perplex['Test Temperature (°C)'] = 25  # Or np.nan if you're planning to fill later
else:
    df_perplex['Test Temperature (°C)'].fillna(25, inplace=True)


# In[526]:


df_perplex.columns


# In[527]:


df_perplex.isnull().sum()


# In[528]:


df_perplex.describe()


# In[529]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[530]:


#Histograms for Distribution
df_perplex.hist(figsize=(15, 10), bins=15, edgecolor='black')
plt.suptitle("Histograms of Numeric Features")
plt.tight_layout()
plt.show()


# In[531]:


#Box Plots for Outliers
plt.figure(figsize=(16, 6))
sns.boxplot(data=df_perplex.select_dtypes(include='number'))
plt.xticks(rotation=45)
plt.title("Box Plot of Numeric Columns")
plt.show()


# In[532]:


plt.figure(figsize=(10, 8))
sns.heatmap(df_perplex.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()


# In[533]:


# Pair Plot (Scatter Matrix)
sns.pairplot(df_perplex.dropna(), corner=True)
plt.suptitle("Pairplot of Numerical Variables", y=1.02)
plt.show()


# In[534]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define all x-y pairs with their interpretation
plot_pairs = [
    ("Grain Size (µm)", "Yield Strength (MPa)", "YS vs Grain Size (colored by Phase)"),
    ("Grain Size (µm)", "UTS (MPa)", "UTS vs Grain Size (colored by Phase)"),
    ("Hardness (HV)", "Yield Strength (MPa)", "YS vs Hardness (colored by Phase)"),
    ("Hardness (HV)", "UTS (MPa)", "UTS vs Hardness (colored by Phase)"),
    ("Dislocation Density (dislocations/m²)", "Yield Strength (MPa)", "YS vs Dislocation Density (colored by Phase)"),
    ("Strain Rate (s⁻¹)", "Elongation (%)", "Elongation vs Strain Rate (colored by Phase)"),
    ("Strain Hardening Exponent (n)", "Strain Hardening Coefficient (k)", "n vs k (colored by Phase)"),
    ("Grain Size (µm)", "Hardness (HV)", "Hardness vs Grain Size (colored by Phase)"),
    ("Yield Strength (MPa)", "Elongation (%)", "Elongation vs YS (colored by Phase)")
]

# Create scatter plots
plt.figure(figsize=(18, 24))  # Adjust height for all subplots
for i, (x, y, title) in enumerate(plot_pairs):
    plt.subplot(3, 3, i+1)
    sns.scatterplot(data=df_perplex, x=x, y=y, hue="Phase")
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()

plt.suptitle("Scatter Plots of Key Mechanical Relationships (colored by Phase)", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# In[535]:


df_perplex.columns


# In[536]:


import matplotlib.pyplot as plt
import seaborn as sns

# Define the category-numeric axis pairs and their titles
violin_pairs = [
    ("Phase", "Hardness (HV)", "Hardness Distribution by Phase"),
    ("Phase", "Yield Strength (MPa)", "Yield Strength Distribution by Phase"),
    ("Phase", "UTS (MPa)", "UTS Distribution by Phase"),
    ("Phase", "Grain Size (µm)", "Grain Size Distribution by Phase"),
    ("Phase", "Elongation (%)", "Elongation Distribution by Phase"),
    ("Phase", "Dislocation Density (dislocations/m²)", "Dislocation Density by Phase"),
    ("Phase", "Strain Rate (s⁻¹)", "Strain Rate Distribution by Phase"),
    ("Phase", "Strain Hardening Exponent (n)", "n (Hardening Exponent) by Phase"),
    ("Phase", "Strain Hardening Coefficient (k)", "k (Hardening Coefficient) by Phase"),
    ("Processing Condition", "Hardness (HV)", "Hardness vs Processing Condition"),
    ("Processing Condition", "Yield Strength (MPa)", "Yield Strength vs Processing Condition"),
    ("Test Temperature (°C)", "Elongation (%)", "Elongation vs Test Temperature"),
]

# Set up the figure
plt.figure(figsize=(20, 20))
for i, (x, y, title) in enumerate(violin_pairs):
    plt.subplot(4, 3, i + 1)
    sns.violinplot(data=df_perplex, x=x, y=y, color='pink', alpha=0.6)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=9)
    plt.ylabel(y, fontsize=9)
    plt.xticks(rotation=45)

plt.suptitle("Violin Plots Showing Distribution of Mechanical Properties Across Categories", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()



# In[537]:


import matplotlib.pyplot as plt
import seaborn as sns

# List of columns for Boxplot with their interpretations
boxplot_columns = [
    ("Elongation (%)", "Phase", "Elongation Distribution by Phase"),
    ("Yield Strength (MPa)", "Phase", "YS Distribution by Phase"),
    ("UTS (MPa)", "Phase", "UTS Distribution by Phase"),
    ("Hardness (HV)", "Phase", "Hardness Distribution by Phase"),
    ("Grain Size (µm)", "Phase", "Grain Size Distribution by Phase"),
    ("Dislocation Density (dislocations/m²)", "Phase", "Dislocation Density Distribution by Phase"),
    ("Strain Rate (s⁻¹)", "Phase", "Strain Rate Distribution by Phase"),
    ("Strain Hardening Exponent (n)", "Phase", "Strain Hardening Exponent Distribution by Phase"),
    ("Strain Hardening Coefficient (k)", "Phase", "Strain Hardening Coefficient Distribution by Phase")
]

# Create boxplots
plt.figure(figsize=(16, 18))  # Adjusting figure size for all subplots
for i, (y, x, title) in enumerate(boxplot_columns):
    plt.subplot(3, 3, i+1)
    sns.boxplot(data=df_perplex, x=x, y=y)
    plt.xticks(rotation=45)
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel(y, fontsize=8)
    plt.tight_layout()

plt.suptitle("Box Plots for Key Mechanical Properties by Phase", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()


# #### ORIGINAL DATASETS

# In[538]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Parse the original data
original_data = [
    {
        "Alloy": "AlCuLiMgAg",
        "Yield Strength (MPa)": 475,  # Used middle of range 450-500
        "UTS (MPa)": 575,  # Used middle of range 550-600
        "Hardness (HV)": 165,  # Used middle of range 150-180
        "Elongation (%)": 10,  # Used middle of range 8-12
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "Al0.5CoCrCuFeNi",
        "Yield Strength (MPa)": 550,
        "UTS (MPa)": 700,
        "Hardness (HV)": 200,
        "Elongation (%)": 15,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "CoCrFeMnNi",
        "Yield Strength (MPa)": 450,
        "UTS (MPa)": 650,
        "Hardness (HV)": 180,
        "Elongation (%)": 35,
        "Test Temperature (°C)": 25,
        "Strain Rate": "NAN"
    },
    {
        "Alloy": "CrMnFeCoNi",
        "Yield Strength (MPa)": 350,
        "UTS (MPa)": 600,
        "Hardness (HV)": 150,
        "Elongation (%)": 50,
        "Test Temperature (°C)": 25,  # Using room temp from the range
        "Strain Rate": "NAN"
    },
    {
        "Alloy": "Al0.5CoCrFeNi",
        "Yield Strength (MPa)": 680,
        "UTS (MPa)": 850,
        "Hardness (HV)": 275,
        "Elongation (%)": 18,
        "Test Temperature (°C)": 25,
        "Strain Rate": "NAN"
    },
    {
        "Alloy": "CoCrFeMnNiV0.5",
        "Yield Strength (MPa)": 420,
        "UTS (MPa)": 680,
        "Hardness (HV)": 195,
        "Elongation (%)": 32,
        "Test Temperature (°C)": 25,
        "Strain Rate": "3e-4"
    },
    {
        "Alloy": "CoCrFeMnNiV1.0",
        "Yield Strength (MPa)": 510,
        "UTS (MPa)": 720,
        "Hardness (HV)": 230,
        "Elongation (%)": 25,
        "Test Temperature (°C)": 25,
        "Strain Rate": "3e-4"
    },
    {
        "Alloy": "CoCrFeMnNi",
        "Yield Strength (MPa)": 250,
        "UTS (MPa)": 500,
        "Hardness (HV)": 135,
        "Elongation (%)": 60,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "CoCrFeNi",
        "Yield Strength (MPa)": 320,
        "UTS (MPa)": 580,
        "Hardness (HV)": 160,
        "Elongation (%)": 50,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "Al0.1CoCrFeNi",
        "Yield Strength (MPa)": 350,
        "UTS (MPa)": 600,
        "Hardness (HV)": 150,
        "Elongation (%)": 55,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "Al0.3CoCrFeNi",
        "Yield Strength (MPa)": 400,
        "UTS (MPa)": 650,
        "Hardness (HV)": 175,
        "Elongation (%)": 45,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "CoCrFeNiTi0.2",
        "Yield Strength (MPa)": 650,
        "UTS (MPa)": 950,
        "Hardness (HV)": 280,
        "Elongation (%)": 25,
        "Test Temperature (°C)": 25,
        "Strain Rate": "NAN"
    },
    {
        "Alloy": "FeCrMnNi",
        "Yield Strength (MPa)": 280,
        "UTS (MPa)": 550,
        "Hardness (HV)": 160,
        "Elongation (%)": 40,
        "Test Temperature (°C)": 25,  # Using room temp
        "Strain Rate": "3e-4"
    },
    {
        "Alloy": "CoCrFeNiPd",
        "Yield Strength (MPa)": 420,
        "UTS (MPa)": 720,
        "Hardness (HV)": 210,
        "Elongation (%)": 38,
        "Test Temperature (°C)": 25,
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "FeCrMnNiCu",
        "Yield Strength (MPa)": 340,
        "UTS (MPa)": 620,
        "Hardness (HV)": 180,
        "Elongation (%)": 45,
        "Test Temperature (°C)": 25,  # Using room temp
        "Strain Rate": "2e-4"
    },
    {
        "Alloy": "CoCrFeNiAl0.3",
        "Yield Strength (MPa)": 480,
        "UTS (MPa)": 750,
        "Hardness (HV)": 220,
        "Elongation (%)": 42,
        "Test Temperature (°C)": 25,  # Using room temp
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "CoCrFeNiPd0.3",
        "Yield Strength (MPa)": 1850,
        "UTS (MPa)": 2100,
        "Hardness (HV)": 620,  # Converting from GPa to HV (approximate)
        "Elongation (%)": 8,
        "Test Temperature (°C)": 25,
        "Strain Rate": "5e-4"
    },
    {
        "Alloy": "Al0.3CoCrFeNi",
        "Yield Strength (MPa)": 700,  # Estimated based on hardness
        "UTS (MPa)": 900,  # Estimated based on hardness
        "Hardness (HV)": 820,  # Converting from GPa to HV (approximate)
        "Elongation (%)": 12,  # Estimated based on similar alloys
        "Test Temperature (°C)": 25,
        "Strain Rate": "NAN"
    },
    {
        "Alloy": "CoCrFeNi",
        "Yield Strength (MPa)": 350,
        "UTS (MPa)": 620,
        "Hardness (HV)": 165,
        "Elongation (%)": 55,
        "Test Temperature (°C)": 25,  # Using room temp
        "Strain Rate": "1e-3"
    },
    {
        "Alloy": "FeCoNiCrCu",
        "Yield Strength (MPa)": 410,
        "UTS (MPa)": 680,
        "Hardness (HV)": 195,
        "Elongation (%)": 32,
        "Test Temperature (°C)": 25,
        "Strain Rate": "NAN"
    }
]

# Convert to DataFrame
df_original = pd.DataFrame(original_data)

# Define common HEA base elements and additives
base_elements = ["Co", "Cr", "Fe", "Ni", "Mn"]
additives = ["Al", "Ti", "Cu", "V", "Mo", "Nb", "Zr", "Si", "B", "C", "N", "W", "Ta", "Hf", "Pd", "Pt", "Au", "Ag"]
strain_rates = ["1e-3", "2e-3", "3e-4", "5e-4", "1e-4", "2e-4", "NAN"]
test_temperatures = [25, -196, -100, -50, 100, 200, 300, 400, 500, 600, 700, 800]

# Function to generate realistic high-entropy alloy compositions
def generate_hea_composition(existing_alloys):
    strategy = random.choice(["mutate", "new_combination"])

    if strategy == "mutate":
        alloy = random.choice(existing_alloys)
        # Simple mutation: add or remove a minor element/concentration
        if random.random() < 0.5:  # Add a small amount of a new element
            additive = random.choice(additives)
            concentration = round(random.uniform(0.1, 0.5), 1)
            if additive not in alloy:
                alloy += additive + str(concentration)
        else:  # Slightly change the concentration of an existing element (if it has a number)
            import re
            numeric_parts = re.findall(r'([A-Za-z]+)(\d+\.\d+|\d+)', alloy)
            if numeric_parts:
                element_to_modify, value = random.choice(numeric_parts)
                original_value = float(value)
                change = round(random.uniform(-0.2, 0.2), 1)
                new_value = max(0.1, min(1.5, original_value + change)) # Keep within reasonable bounds
                alloy = alloy.replace(element_to_modify + value, element_to_modify + str(new_value))
        return alloy
    else: # new_combination
        num_elements = random.randint(3, 6)
        elements = random.sample(base_elements + additives, num_elements)
        elements.sort()
        new_alloy = ""
        for el in elements:
            if el in additives and random.random() < 0.6: # Add concentration for some additives
                new_alloy += el + str(round(random.uniform(0.1, 1.0), 1))
            else:
                new_alloy += el
        return "".join(new_alloy)

# Function to generate coherent mechanical properties, influenced by original data
def generate_properties(original_df):
    # Sample a data point from the original data to get a baseline
    baseline = original_df.sample(n=1).iloc[0]

    # Introduce some variation around the baseline values
    ys = int(baseline['Yield Strength (MPa)'] * random.uniform(0.8, 1.2))
    uts = int(baseline['UTS (MPa)'] * random.uniform(0.8, 1.2))
    hardness = int(baseline['Hardness (HV)'] * random.uniform(0.8, 1.2))
    elongation = round(baseline['Elongation (%)'] * random.uniform(0.8, 1.2), 1)
    temp = random.choice(test_temperatures)
    strain_rate = random.choice(strain_rates)

    # Add some more random variation to explore a wider space
    if random.random() < 0.3:
        ys += random.randint(-100, 100)
    if random.random() < 0.3:
        uts += random.randint(-150, 150)
    if random.random() < 0.3:
        hardness += random.randint(-50, 50)
    if random.random() < 0.3:
        elongation += random.uniform(-10, 10)

    ys = max(50, ys)
    uts = max(ys + 50, uts)
    hardness = max(50, hardness)
    elongation = max(1, elongation)

    return {
        "Yield Strength (MPa)": int(ys),
        "UTS (MPa)": int(uts),
        "Hardness (HV)": int(hardness),
        "Elongation (%)": round(elongation, 1),
        "Test Temperature (°C)": temp,
        "Strain Rate": strain_rate
    }

# Generate 60 new synthetic data points
original_data = []
existing_alloys = df_original['Alloy'].unique().tolist()
for _ in range(60):
    alloy = generate_hea_composition(existing_alloys)
    properties = generate_properties(df_original)
    original_data.append({**{"Alloy": alloy}, **properties})

df_origin = pd.DataFrame(original_data)
print("df_origin (first 5 rows):\n", df_origin.head())


# In[539]:


df_origin.rename(columns={'Strain Rate': 'Strain Rate (s⁻¹)'}, inplace=True)


# In[540]:


df_origin.head(60)


# #### Comparative graphs between original vs AI datasets

# In[546]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



# --- 1. Data Preparation for Plotting ---

# Function to melt the dataframe for easier plotting with seaborn
def melt_dataframe(df, model_name):
    """Melts the dataframe to a long format for plotting."""
    melted_df = pd.melt(
        df,
        id_vars=['Alloy', 'Test Temperature (°C)','Strain Rate (s⁻¹)'],
        value_vars=['Yield Strength (MPa)', 'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)'],
        var_name='Property',
        value_name='Value'
    )
    melted_df['Model'] = model_name
    return melted_df

# Melt all dataframes
df_original_melted = melt_dataframe(df_origin, 'Original Data')
df_chatgpt_melted = melt_dataframe(df_chatgpt, 'ChatGPT')
df_claude_melted = melt_dataframe(df_claude, 'Claude')
df_perplexity_melted = melt_dataframe(df_perplex, 'Perplexity')
df_gemini_melted = melt_dataframe(df_gemini, 'Gemini')

# Combine all melted dataframes
df_combined = pd.concat([
    df_original_melted,
    df_chatgpt_melted,
    df_claude_melted,
    df_perplexity_melted,
    df_gemini_melted
], ignore_index=True)

# Convert 'Value' to numeric, handling potential ranges (taking the average)
def handle_value(value):
    if isinstance(value, str) and '–' in value:
        low, high = map(float, value.split('–'))
        return (low + high) / 2
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

df_combined['Value_Numeric'] = df_combined['Value'].apply(handle_value)
df_combined = df_combined.dropna(subset=['Value_Numeric'])



# In[547]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



properties_to_plot = ['Yield Strength (MPa)', 'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)']

for prop in properties_to_plot:
    plt.figure(figsize=(8, 6))
    sns.boxplot(
        x='Model',
        y='Value_Numeric',
        data=df_combined[df_combined['Property'] == prop],
        palette='viridis'
    )
    plt.title(f'Distribution of {prop} - Original Data vs. AI Models')
    plt.xlabel('Model')
    plt.ylabel(prop)
    plt.tight_layout()
    plt.show()


# In[548]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



properties_to_plot = ['Yield Strength (MPa)', 'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)']

for prop in properties_to_plot:
    plt.figure(figsize=(8, 6))
    sns.pointplot(
        x='Model',
        y='Value_Numeric',
        data=df_combined[df_combined['Property'] == prop],
        capsize=0.2  # Add error bars
    )
    plt.title(f'Mean and Standard Deviation of {prop} - Original Data vs. AI Models')
    plt.xlabel('Model')
    plt.ylabel(prop)
    plt.tight_layout()
    plt.show()


# #### Interactive Plot with Plotly:

# In[549]:


import pandas as pd
import plotly.express as px


properties_to_plot = ['Yield Strength (MPa)', 'UTS (MPa)', 'Hardness (HV)', 'Elongation (%)']

for prop in properties_to_plot:
    fig = px.bar(
        df_combined[df_combined['Property'] == prop],
        x='Alloy',
        y='Value_Numeric',
        color='Model',
        title=f'Comparison of {prop} - Original Data vs. AI Models',
        labels={'Value_Numeric': prop, 'Alloy': 'Alloy Composition'},
        barmode='group'  # or 'relative'
    )
    fig.update_layout(xaxis={'tickangle': -45, 'automargin': True})
    fig.show()
    


# In[ ]:




