import json
import math

# from nsga2.problem import Problem
# from nsga2.evolution import Evolution
from problem import Problem
from evolution import Evolution
import time
def getScore(params=None, post=None):
    """ Tính điểm cho bài post với bộ tham số `params`
    Điểm sẽ được cập nhật thẳng vào bài post

    :Args:
    - params - tuple chứa 5 phần tử lần lượt là các tham số (H1, H2, H3, K2, K2)

    :Rets:
    - không trả về
    """
    H1, H2, H3, K1, K2 = params

    post['score'] = H1 * post['diem_max_phuongantaichinh'] + \
                    H2 * post['diem_trungbinh_phuongantaichinh'] + \
                    H3 * (K1 * 10 * post['tile_phuongantaichinh_phuhop'] + K2 * post['diem_scaled_soluong_phuongantaichinh'])
   
def optimizator(nGeneration=1000, nVariables=1, objectives=None, varRange=None, same_range=None):
    """Hàm tìm bộ tham số tối ưu để tối thiểu hóa các hàm `objectives`

    Keyword Arguments:
        nGeneration {int} -- Số lượng thế hệ muốn chạy tìm tối ưu (default: {1000})
        nVariables {int} -- Số lượng biến trong hàm tối ưu (default: {1})
        objectives {list} -- Danh sách các hàm cần tối ưu (default: {None})
        varRange {list} -- Danh sách các tuple là khoảng giá trị của các biến trong các hàm `objectives` (default: {None})

    Returns:
        list, list -- danh sách các giá trị của biến khiến các hàm `objectives` đạt tối thiểu, danh sách các giá trị tối thiểu của các hàm
    """


    ##############################
    # Định nghĩa problem cần minimize
    ##############################
    problem = Problem(
        num_of_variables=nVariables,
        objectives=objectives,
        variables_range=varRange,
        same_range=same_range)


    ##############################
    # Tiến hành minimize
    ##############################
    evo = Evolution(problem, num_of_generations=nGeneration)
    evol = evo.evolve()

    return evol[0].features, evol[0].objectives




if __name__ == "__main__":
    print("1. Đọc data từ file 'data.json'")
    with open("data.json", 'r') as dat_file:
        list_posts = json.load(dat_file)
    start = time.clock()


    ##########################################################
    # Tiến hành tìm bộ tham số tối ưu
    ##########################################################
    print("2. Tiến hành tối ưu")


    def optimizator_kernel(*args):
        """Đây chính là hàm objective để chạy tối ưu NSGA-2

        Returns:
            [type] -- [description]
        """
        H1, H2, H3, K1, K2 = args


        ####################################
        ## Tính toán lại các tham số
        ####################################
        s = (H1 + H2 + H3) if (H1 + H2 + H3) > 0 else 1
        H1 = H1 / s
        H2 = H2 / s
        H3 = H3 / s
        s = (K1 + K2) if (K1 + K2) > 0 else 1
        K1 = K1 / s
        K2 = K2 / s


        ####################################
        ## Tính điểm cho từng bài post
        ####################################
        for post in list_posts:
            getScore(params=(H1, H2, H3, K1, K2), post=post)


        ####################################
        ## Sắp xếp các bài post
        ####################################
        list_posts.sort(key=lambda x:x['score'], reverse=True)


        ####################################
        ## Tính fitness level cho bộ tham số
        ####################################
        # result = math.sqrt(sum([(i - post['rank'])**2 for i, post in enumerate(list_posts)]))
        # if result == 0:
        #     return 10**9
        # else:
        #     return result
        return math.sqrt(sum([(i - post['rank'])**2 for i, post in enumerate(list_posts)]))


    param_set, score = optimizator(
        nGeneration=1000,
        nVariables=5,
        objectives=[optimizator_kernel],
        varRange=[(0, 100)],
        same_range=True)


    ##########################################################
    # Trả về kết quả
    ##########################################################
    print("3. In kết quả")

    print("* Bộ tham số đã tối ưu             : {}".format(param_set))
    print("* Giá trị của metric dùng để tối ưu: {:6.3f}".format(score[0]))
    i = 0
    for post in list_posts:
        i = i+1
        print("- Post: {:>10} has score: {:6.3f}".format(post['post_id'], post['score']))
        if i > 20:
            break
    end = time.clock()
    print(end - start)
