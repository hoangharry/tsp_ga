
from problem import Problem
from evolution import Evolution

def optimizator(nGeneration=1000, nIndividuals=1000, nVariables=1, objectives=None, varRange=None, same_range=None):
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
    evo = Evolution(problem, num_of_generations=nGeneration, num_of_individuals=nIndividuals)
    evol = evo.evolve()

    return evol[0].features, evol[0].objectives

if __name__ == "__main__":
    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    distances = []
    with open('data_5cities.txt', 'r') as dat_file:
        n = 5
        for line in dat_file.readlines():
            distances.append([float(line[i:i+n]) for i in range(0, len(line) - 1, n)])



    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    def kernel_optimizator(*args):
        ''' Đây là hàm nhân (kernel) của GA

        :Args:
        None

        :Rets:
        float - là fitness level của bộ tham số H1, H2, K1, K2, K3
        '''

        list_cities = []

        ####################################
        ## Biến các input thành số nguyên và loại bỏ
        ## các gen không tốt
        ####################################
        for x in args:
            tmp = int(x)
            if tmp not in list_cities:
                list_cities.append(tmp)
            else:
                flag = False
                for k in range(tmp + 1, len(args), 1):
                    if k not in list_cities:
                        list_cities.append(k)
                        flag = True
                        break
                if not flag:
                    for k in range(tmp - 1, -1, -1):
                        if k not in list_cities:
                            list_cities.append(k)
                            break


        cul_distance = distances[list_cities[0]][list_cities[len(list_cities) - 1]]
        ####################################
        ## Tính toán đường đi
        ####################################
        for i in range(1, len(list_cities), 1):
            cul_distance += distances[list_cities[i - 1]][list_cities[i]]

        return cul_distance


    params, objectives = optimizator(
        nGeneration=30,
        nVariables=5,
        objectives=[kernel_optimizator],
        varRange=[(0, 4.9)],
        same_range=True,
        nIndividuals=500
    )


    print("Params    : {}".format(params))
    print("Objectives: {}".format(objectives))
