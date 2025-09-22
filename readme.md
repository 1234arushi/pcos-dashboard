# PCOS Dashboard Project
This project analyzes a PCOS dataset and builds an interactive dashboard using Streamlit.

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
  - recall : of actuall pcos patients,the model finds 75%(imp as we do not want to miss the women having pcos)

- **After adding custom threshold & (using class_weight = "balanced")**  
  - recall : 83 %
