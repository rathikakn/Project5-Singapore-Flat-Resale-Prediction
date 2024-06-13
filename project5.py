import streamlit as st
from streamlit_option_menu import option_menu

import numpy as np
import datetime
import pickle


#set up page configuration for streamlit
st.set_page_config(page_title='Singapore Flat Resale Price Predictor',page_icon='house',
                        layout='wide')

#css for page setup
st.markdown("""
    <style>
    .main-menu {font-size:20px; margin-top:-40px;}
    .content {padding: 20px;}
    .header {margin-top: 20px; padding-top: 30px; text-align: center; background-color:#002b36 ; padding-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

c1,_,c2=st.columns([2,1,2])

#set up the sidebar with optionmenu
selected = option_menu(
    menu_title="Singapore  Resale Flat Prices Predicting",  
    options=["Home", "Flat Resale Price Prediction"], 
    icons=['house', "info-circle"],  
    default_index=0, 
    orientation="horizontal",
    )

#user input values for selectbox and encoded for respective features
class option:

    option_months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    encoded_month= {"January" : 1,"February" : 2,"March" : 3,"April" : 4,"May" : 5,"June" : 6,"July" : 7,"August" : 8,"September" : 9,
            "October" : 10 ,"November" : 11,"December" : 12}

    option_town=['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH','BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
        'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST','KALLANG/WHAMPOA', 'MARINE PARADE', 'QUEENSTOWN', 'SENGKANG','SERANGOON',
        'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN','LIM CHU KANG', 'SEMBAWANG', 'BUKIT PANJANG', 'PASIR RIS','PUNGGOL']
    
    encoded_town={'ANG MO KIO' : 0 ,'BEDOK' : 1,'BISHAN' : 2,'BUKIT BATOK' : 3,'BUKIT MERAH' : 4,'BUKIT PANJANG' : 5,'BUKIT TIMAH' : 6,
        'CENTRAL AREA' : 7,'CHOA CHU KANG' : 8,'CLEMENTI' : 9,'GEYLANG' : 10,'HOUGANG' : 11,'JURONG EAST' : 12,'JURONG WEST' : 13,
        'KALLANG/WHAMPOA' : 14,'LIM CHU KANG' : 15,'MARINE PARADE' : 16,'PASIR RIS' : 17,'PUNGGOL' : 18,'QUEENSTOWN' : 19,
        'SEMBAWANG' : 20,'SENGKANG' : 21,'SERANGOON' : 22,'TAMPINES' : 23,'TOA PAYOH' : 24,'WOODLANDS' : 25,'YISHUN' : 26}
    
    option_flat_type=['1 ROOM', '2 ROOM','3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE','MULTI-GENERATION']

    encoded_flat_type={'1 ROOM': 0,'2 ROOM' : 1,'3 ROOM' : 2,'4 ROOM' : 3,'5 ROOM' : 4,'EXECUTIVE' : 5,'MULTI-GENERATION' : 6}

    option_flat_model=['2-ROOM','3GEN','ADJOINED FLAT', 'APARTMENT' ,'DBSS','IMPROVED' ,'IMPROVED-MAISONETTE', 'MAISONETTE',
                    'MODEL A', 'MODEL A-MAISONETTE','MODEL A2' ,'MULTI GENERATION' ,'NEW GENERATION', 'PREMIUM APARTMENT',
                    'PREMIUM APARTMENT LOFT', 'PREMIUM MAISONETTE','SIMPLIFIED', 'STANDARD','TERRACE','TYPE S1','TYPE S2']

    encoded_flat_model={'2-ROOM' : 0,'3GEN' : 1,'ADJOINED FLAT' : 2,'APARTMENT' : 3,'DBSS' : 4,'IMPROVED' : 5,'IMPROVED-MAISONETTE' : 6,
                'MAISONETTE' : 7,'MODEL A' : 8,'MODEL A-MAISONETTE' : 9,'MODEL A2': 10,'MULTI GENERATION' : 11,'NEW GENERATION' : 12,
                'PREMIUM APARTMENT' : 13,'PREMIUM APARTMENT LOFT' : 14,'PREMIUM MAISONETTE' : 15,'SIMPLIFIED' : 16,'STANDARD' : 17,
                'TERRACE' : 18,'TYPE S1' : 19,'TYPE S2' : 20}
    sorted_lease_commence_year=[1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 
                                1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 
                                2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 
                                2017, 2018, 2019, 2020]
    lease_year_remaining=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                          31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                          61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 
                          91, 92, 93, 94, 95, 96, 97, 98, 99]
    
    selling_year=[2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 
                  2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 
                  1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966]
    
    block_numbers=[309, 216, 211, 202, 235, 232, 308, 220, 219, 247, 320, 252, 223,
       230, 329, 313, 117, 110, 343, 345, 346, 121, 129, 130, 128, 127,
       126, 403, 404, 405, 417, 418, 419, 441, 442, 443, 444, 450, 435,
       433, 434, 424, 425, 466, 471, 474, 570, 586, 455, 465, 463, 564,
       560, 558, 559, 538, 534, 601, 603, 604, 608, 611, 505, 503, 610,
       607, 524, 513, 643, 542, 548, 550, 639, 637, 330, 333, 156, 152,
       178, 180, 209, 231, 254, 103, 105, 344, 324, 120, 124, 414, 438,
       427, 428, 473, 573, 585, 456, 544, 640, 638, 646, 150, 179, 336,
       335, 401, 439, 430, 460, 459, 716, 545, 620, 622, 259, 101,  18,
        28,  29,  30,  75,  76, 501, 502, 504,   2,  20,  21,  59,  58,
        55,  22, 104, 107,  69,  33,  46, 116, 115, 125, 138,  87, 100,
       412, 402, 416, 136, 529, 510, 525, 218, 213, 532, 533, 536, 537,
        44, 540, 702, 615, 712,  50,  54, 606, 616,  15,  34,  36,  35,
        41,  42,  53,  51,   8, 718, 724, 166,  71,  82,  78,  79,  80,
       134, 132, 131, 133,  89,  62, 422, 507, 508, 517,  95,  93,  43,
       543, 547, 708, 707, 713, 609,  61,  56, 165, 710, 613, 602, 605,
       112,   1, 722,  72,  31, 111, 118,  96, 137, 139, 725,  24, 304,
       310, 160, 161, 164, 177, 205, 248, 258,   4,   6, 146, 143, 145,
       182, 228, 227, 244, 113, 163, 169, 204, 135, 184, 225, 123, 307,
       221, 214, 142, 140, 141,   7,  40,  77, 119, 114,   5,  12,  16,
        13, 108, 102, 106,  63,  60,   3,  19,  26,  37,  47, 109,  57,
        48,  73,  66, 264, 271, 664,   9,  10, 663, 662, 632, 633, 642,
       440, 509, 363, 365, 334, 323, 322, 326, 314, 312, 354, 506, 305,
       306, 303, 431, 339, 515, 520, 703, 704, 711, 705, 731, 728, 706,
       411, 315, 311, 301, 729, 371, 415, 413, 337, 717, 723, 201,  81,
        45,  85,  98,  99,  65,  23,  67,  49,  39,  38,  17, 319, 318,
       327, 410, 239, 154, 341, 352, 251, 302, 234, 237, 233, 242, 243,
       257, 210, 208, 316, 408, 240, 331, 406, 167, 168, 170, 172, 185,
       186, 187, 212, 215, 516, 511, 457, 490, 489, 487, 485, 476, 477,
       527, 535, 484, 491, 481, 217, 448, 446, 447, 554, 551, 458, 436,
       452, 539, 198, 203, 407, 469, 468, 801,  97,  11,  68,  94,  14,
        84,  83,  52, 807, 461,  32, 171, 173,  88,  86,  74,  25, 267,
       269, 924, 925, 817, 818, 808, 809, 285, 287, 274, 291, 293, 262,
       914, 250, 226, 236, 270, 420, 157, 820, 819, 813, 810, 266, 265,
       286, 272, 275, 295, 261, 913, 910, 253, 277, 928, 832, 838, 839,
       159, 812, 811, 294, 432, 816, 289, 298, 912, 278, 279, 245, 149,
       148,  91,  27, 206, 193, 200, 162, 701, 736, 742, 276, 751, 752,
       733, 740, 280, 772, 229, 238, 255, 256, 328, 348, 571, 584, 454,
       575, 561, 512, 523, 644, 621, 625, 155, 470, 565, 546, 612, 648,
        70, 122, 426, 530, 519, 526, 626, 709, 719, 207, 175, 249, 260,
       183, 641, 362, 409, 429, 518, 449, 379, 359, 347, 342, 340, 846,
       317, 321, 325, 357, 241, 462, 475, 528, 480, 514, 437, 451, 486,
       199,  64, 153,  90, 224, 814, 283, 297, 848, 831, 281, 273, 916,
       902, 921, 934, 268, 805, 833, 804, 903, 932, 151, 147, 174, 195,
       222, 741, 756, 390, 737, 726, 358, 421, 445, 587, 464, 557, 549,
       624, 631, 572, 563, 552, 522, 614, 715, 714, 144, 661, 634, 730,
       338, 349, 351, 353, 246, 521, 488, 478, 555, 556, 907, 282, 292,
       935, 263, 933, 926, 922, 191, 732, 158, 727, 721, 284, 759, 858,
       576, 578, 541, 623, 332, 423, 176, 181, 668, 364, 374, 350, 373,
       381, 355, 531, 483, 553, 909, 930, 915, 911, 931, 815, 194, 754,
       749, 618,  92, 628, 472, 806, 837, 290, 296, 857, 735, 746, 649,
       635, 636, 367, 360, 376, 854, 288, 747, 738, 768, 757, 467, 562,
       617, 627, 361, 368, 370, 479, 852, 745, 771, 766, 773, 755, 758,
       577, 619, 720, 377, 356, 842, 453, 803, 937, 762, 739, 774, 760,
       366, 375, 844, 734, 778, 197, 369, 929, 830, 856, 764, 744, 684,
       908, 765, 686, 683, 840, 783, 784, 750, 770, 495, 835, 685, 682,
       853, 753, 781, 775, 657, 776, 498, 824, 847, 378, 645, 681, 841,
       782, 388, 674, 675, 845, 851, 785, 372, 673, 482, 836, 788, 189,
       829, 843, 800, 629, 630, 676, 761, 655, 794, 790, 689, 492, 748,
       795, 796, 799, 196, 696, 849, 798, 791, 494, 897, 855, 802, 779,
       190, 688, 658, 660, 687, 697, 827, 777, 743, 651, 647, 695, 698,
       693, 694, 665, 828, 906, 653, 867, 667, 680, 763, 780, 671, 690,
       883, 792, 192, 669, 977, 944, 691, 917, 825, 895, 672, 650, 884,
       821, 881, 885, 882, 393, 394, 666, 656, 399, 386, 391, 652, 862,
       864, 863, 860, 659, 868, 859, 861, 397, 786, 787, 826, 877, 834,
       876, 678, 898, 878, 767, 872, 880, 874, 380, 677, 870, 871, 865,
       866, 879, 797, 875, 389, 850, 920, 387, 392, 904, 949, 395, 396,
       822, 886, 873, 670, 899, 692, 978, 887, 939, 905, 927, 894, 679,
       936, 919, 896, 188, 923, 888, 938, 654, 943, 940, 942, 398, 769,
       966, 945, 889, 941, 947, 946, 918, 869, 976, 979, 567, 948, 953,
       789, 980, 823, 974, 496, 965, 975, 952, 961, 500, 950, 382, 568,
       385, 793, 497, 893, 566, 569, 493, 384, 383, 580, 579, 700, 581,
       583, 582, 574, 891, 892, 299, 300, 962, 699, 956, 951, 957, 958,
       955, 954, 964, 959, 963, 969, 968, 970, 960, 973, 972, 971, 967,
       596, 588, 589, 981, 984, 985, 986, 989, 987, 988, 990, 499, 590,
       591, 592, 593, 890, 997, 992, 998, 991, 996, 995, 999]

#set up information for the 'prediction' menu
if selected == "Flat Resale Price Prediction":
    st.write('')
    st.markdown("<h5 style=color:red>Please Provide the below Information to Predict the Resale Price of a Flat:",unsafe_allow_html=True)
    st.write('')

    # creted form to get the user input 
    with st.form('prediction'):
        col1,col2=st.columns(2)
        with col1:

            user_flat_type=st.selectbox(label='Flat Type',options=option.option_flat_type,index=None)
            
            block=st.selectbox(label='Block',options=option.block_numbers,index=None)
            
            year=st.selectbox(label='year',options=option.selling_year,index=None)

            user_flat_model=st.selectbox(label='Flat Model',options=option.option_flat_model,index=None)

            remaining_lease=st.selectbox(label='Remaining lease year',options=option.lease_year_remaining,index=None)

            price_per_sqm=st.number_input(label='Price Per sqm',min_value=100.00)

        with col2:

            user_month=st.selectbox(label='Month',options=option.option_months,index=None)

            user_town=st.selectbox(label='Town',options=option.option_town,index=None)

            lease_commence_date=st.selectbox(label='Year of lease commence',options=option.sorted_lease_commence_year,index=None)
            
            floor_area_sqm=st.number_input(label='Floor area sqm',min_value=10.0)

            years_holding=st.number_input(label='Years Holding',min_value=0,max_value=99)

            c1,c2=st.columns(2)
            with c1:
                storey_start=st.number_input(label='Storey start',min_value=1,max_value=50)
            with c2:
                storey_end=st.number_input(label='Storey end',min_value=1,max_value=51)
            
            st.markdown('<br>', unsafe_allow_html=True)

            button=st.form_submit_button('PREDICT VALUE',use_container_width=True)

    if button:

        #check whether user fill all required fields
        if not all([user_month,user_town,user_flat_type,user_flat_model,floor_area_sqm,price_per_sqm,year,block,
                    lease_commence_date,remaining_lease,years_holding,storey_start,storey_end]):
            st.error("Please fill in all required fields.")

        else:
            #create features from user input 
            current_year=datetime.datetime.now().year

            current_remaining_lease=remaining_lease-(current_year-(int(year)))
            age_of_property=current_year-int(lease_commence_date)


            month=option.encoded_month[user_month]
            town=option.encoded_town[user_town]
            flat_type=option.encoded_flat_type[user_flat_type]
            flat_model=option.encoded_flat_model[user_flat_model]

            floor_area_sqm_log=np.log(floor_area_sqm)
            remaining_lease_log=np.log1p(remaining_lease)
            price_per_sqm_log=np.log(price_per_sqm)

            #opened pickle model and predict the resale price with user data
            with open('Decisiontree.pkl','rb') as files:
                model=pickle.load(files)
            
            user_data=np.array([[month, town, flat_type, block, flat_model, lease_commence_date, year, storey_start,
                                    storey_end, years_holding, current_remaining_lease, age_of_property, floor_area_sqm_log, 
                                    remaining_lease_log,price_per_sqm_log ]])
            #current_remaining_lease

            predict=model.predict(user_data)
            resale_price=np.exp(predict[0])

            #display the predicted selling price 
            st.subheader(f"Predicted Resale price is: :green[{resale_price:.2f}]")

#set up information for 'About' menu 
if selected == "Home":
    st.subheader(':red[Project Title :]')
    st.markdown('<h5>  Singapore Resale Flat Prices Predicting',unsafe_allow_html=True)

    st.subheader(':red[Domain :]')
    st.markdown('<h5>Real Estate',unsafe_allow_html=True)

    st.subheader(':red[Skills & Technologies :]')
    st.markdown('<h5> Python scripting, Data Preprocessing,  EDA, Machine learning, Streamlit ',unsafe_allow_html=True)

    st.subheader(':red[Scope :]')
    st.markdown('''  <h6>Data Collection and Preprocessing:  <br>     
                <li> Collect a dataset of resale flat transactions from the Singapore Housing and Development Board (HDB) for the years 1990 to Till Date. 
                Preprocess the data to clean and structure it for machine learning.<br>              
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Feature Engineering:  <br>     
                <li> Extract relevant features from the dataset, including town, flat type, storey range, floor area, flat model, and lease commence date. 
                Create any additional features that may enhance prediction accuracy.<br>              
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Model Selection and Training:  <br>     
                <li> Choose an appropriate machine learning model for regression (e.g., linear regression, decision trees, or random forests). 
                Train the model on the historical data, using a portion of the dataset for training.<br>              
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Model Evaluation:  <br>     
                <li> Evaluate the model's predictive performance using regression metrics such as Mean Absolute Error (MAE), 
                Mean Squared Error (MSE), or Root Mean Squared Error (RMSE) and R2 Score.<br>              
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Streamlit Web Application:   <br>     
                <li> Develop a user-friendly web application using Streamlit that allows users to input details of a flat (town, flat type, storey range, etc.). 
                Utilize the trained machine learning model to predict the resale price based on user inputs.<br>  
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Deployment on Render: <br>     
                <li> Deploy the Streamlit application on the Render platform to make it accessible to users over the internet.<br>              
                ''',unsafe_allow_html=True)
    st.markdown('''  <h6>Testing and Validation:  <br>     
                <li> Thoroughly test the deployed application to ensure it functions correctly and provides accurate predictions.<br>              
                ''',unsafe_allow_html=True)
    
    