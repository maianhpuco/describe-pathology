# describe-patholog
```
<!-- export PROJECT_DIR =$(pwd) -->
```




Datasets: 
DataPath: contain report level (caption and raw pdf report of the dataset in TCGA)
already download: 
- TCGA-BRCA

/project/hnguyen2/hqvo3/Datasets/digital_pathology/public/TCGA-BRCA 
/project/hnguyen2/mvu9/datasets/PathText/TCGA-BRCA/ 

## TCGA Datasets with Whole Slide Images

| Dataset Folder | Cancer Type                             | Notes                                                             |
|----------------|------------------------------------------|-------------------------------------------------------------------|
| TCGA-BRCA      | Breast Invasive Carcinoma                | Most common; includes IDC, ILC; well-annotated                    |
| TCGA-LUAD      | Lung Adenocarcinoma                      | Frequently used; many paired reports available                    |
| TCGA-LUSC      | Lung Squamous Cell Carcinoma             | Often used with LUAD; clear histological difference               |
| TCGA-COAD      | Colon Adenocarcinoma                     | Digestive system; consistent pathology slides                     |
| TCGA-READ      | Rectum Adenocarcinoma                    | Often grouped with COAD for colorectal cancer studies             |
| TCGA-KIRC      | Kidney Renal Clear Cell Carcinoma        | Well-structured WSIs; common renal cancer dataset                 |
| TCGA-UCEC      | Uterine Corpus Endometrial Carcinoma     | High-grade endometrial carcinoma with text and WSI support        |
| TCGA-OV        | Ovarian Serous Cystadenocarcinoma        | Limited WSIs, but useful for ovarian cancer research              |
| TCGA-THCA      | Thyroid Carcinoma                        | Clean histology; useful for glandular tissue analysis             |
| TCGA-LGG       | Lower Grade Glioma                       | Often paired with GBM; for brain tumor classification             |
| TCGA-GBM       | Glioblastoma Multiforme                  | Aggressive brain cancer; rich in genomic and histology features   |


TCGA-RCC : Renal Cell Carcinoma (KIRC, KIRP, KICH) 
TCGA-NSCLC : Non-Small Cell Lung Cancer (LUAD, LUSC) 

## Classification label download: 
- https://portal.gdc.cancer.gov/projects/TCGA-BRCA -> click on Clinical 



## TCGA-BRCA SUMMARY:
[INFO] Unique diagnosis labels:
['Infiltrating duct carcinoma, NOS' 'Adenoid cystic carcinoma'
 'Apocrine adenocarcinoma' 'Intraductal carcinoma, noninfiltrating, NOS'
 'Not Reported' 'Lobular carcinoma, NOS'
 'Infiltrating duct and lobular carcinoma'
 'Infiltrating duct mixed with other types of carcinoma'
 'Infiltrating lobular mixed with other types of carcinoma'
 'Intraductal papillary adenocarcinoma with invasion' 'Carcinoma, NOS'
 'Invasive micropapillary carcinoma' 'Tubular adenocarcinoma'
 'Cribriform carcinoma, NOS' 'Clear cell carcinoma'
 'Metaplastic carcinoma, NOS' 'Medullary carcinoma, NOS'
 'Mucinous adenocarcinoma' 'Pleomorphic carcinoma'
 'Lobular carcinoma in situ, NOS'
 'Paget disease and infiltrating duct carcinoma of breast'
 'Adenocarcinoma, NOS' 'Phyllodes tumor, malignant'
 'Papillary carcinoma, NOS' 'Large cell neuroendocrine carcinoma'
 'Basal cell carcinoma, NOS' 'Myelodysplastic syndrome, NOS']
[INFO] Total number of unique labels: 27

[INFO] Captions summary:
  Available reports : 1061
  Missing reports   : 37  