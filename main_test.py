from generation.generate import main as main_generate
from services.draw_service import main_draw
from services.file_service import load_item_file, delete_user_file, delete_item_file
from services.item_functions.item_service import *
from services.user_functions.user_service import *


if __name__ == "__main__":
    # print("---{=======}---")
    # test_settings()
    # print("---{=======}---")
    # test_file_service()
    # print("---{=======}---")
    # test_user_generation()
    # print("---{=======}---")
    # test_user_retrieval()
    # print("---{=======}---")
    # test_item_service()
    # print("---{=======}---")
    n = 8
    main_generate(n)
    
    reserve_item(2, 9)
    
    # import time
    
    # s1 = time.time()
    # for _ in range(n//2) :
    #     main_draw(_ + 1)
        
    # s2 = time.time()
    # print((s2 - s1)/n)
    # # print(main_draw(1))
    
    # delete_user(2)
    # delete_item(1)
    
    # # print_all_users()
    
    # for _ in range(n) :
    #     main_draw(_ + 1)