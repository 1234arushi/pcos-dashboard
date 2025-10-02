# PCOS Dashboard Project
A full-stack **PCOS Screening Dashboard** built with **Streamlit (UI)**, **FastAPI (Backend)**, and **PostgreSQL (Database)**.  
The system allows clinicians to enter patient data, automatically compute BMI, predict **PCOS risk probability** and view patient history.


- **Cycle Type & PCOS**  
  - ~62% of women with **irregular cycles** had PCOS.  
  - Only ~21% of women with **regular cycles** had PCOS.  

- **BMI & PCOS**  
  - Non-PCOS women: BMI mostly in **normal range (~23)**.  
  - PCOS women: BMI shifted to **overweight range (~25–30)**.  

- **Symptoms strongly associated with PCOS**  
  1. Weight gain
  2. Excess hair growth (hirsutism)
  3. Skin darkening 

- **Lifestyle factors**  
  - Eating fast food increases PCOS risk.  
  - Regular exercise reduces PCOS prevalence.  

- **Model Results**  
  - accuracy : 86%
  - precision : when the model says PCOS = 1,it is correct 82% of 
    the time
  - recall : of actuall pcos patients,the model finds 75% 

- **After adding custom threshold & (using class_weight = "balanced")**  
  - recall : 83 %
  
- **Threshold Optimization:**
  - Used ROC curve + Youden’s J statistic to select best probability cutoff (≈0.49)
  - recall : 81 %
