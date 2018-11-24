from sympy import *
import math
def main():
    print("Построение регрессионной модели")
    countArgsAi = int(input('Введите количество параметров Ai линейной функции :'))
    argsAi = symbols('a0:%d' % countArgsAi)   
    #pathToFile = input("Введите абсолютый путь к файлу с входными данными :")
    pathToFile = 'inputData.txt'
    try:
        inputFile = open(pathToFile, "r")
        try:
            matrixInputData = inputFile.readlines()
        except Exception as  e:
            print('Ошибка при чтении файла, программа будет закрыта')
            return 1
        finally:
            inputFile.close()
    except Exception as ex:
        print("Такого файла не существует, программа будет закрыта")
        return 1
    
    countRows = len(matrixInputData)
    for indexRow in range(0,len(matrixInputData)):
        matrixInputData[indexRow] = matrixInputData[indexRow].strip()
        matrixInputData[indexRow] = matrixInputData[indexRow].split(' ')
    countColumns = len(matrixInputData[0])
    if countRows < 5 or countColumns < 3:
        print('Для задачи недостаточно входных данных')
        return 1
    if countColumns != countArgsAi:
        print('Количество аргументов Xi не соответствует количеству аргументов Ai')
        return 1
    
    funcError = getFuncError(matrixInputData,argsAi, countArgsAi)
    gradFuncError = getGradFunc(funcError,argsAi)
    solution = solve(gradFuncError,argsAi)
    for i in range(0,countArgsAi):
        funcError = funcError.replace(str(argsAi[i]), str(solution[argsAi[i]]))
    valueFuncError = eval(funcError)
    disp = sqrt(valueFuncError / (countRows - (countArgsAi - 1) - 1))
    funcForSigma = getFuncForSigma(funcError)
    sigma = 0
    for i in range(0,countRows):
        sigma+=math.fabs(eval(funcForSigma[i]) / int(matrixInputData[i][0]))
    sigma = sigma * 100 / countRows
        
    print("Искомые параметры Ai:")
    for i in  range(0,countArgsAi):
        print(str(argsAi[i]) + ':' + str(solution[argsAi[i]]))
    print('Остаточная дисперсия D=' + str(disp))
    print('Средняя относительная ошибка SIGMA=' + str(sigma))
    print('Дисперсия среднего=' + str(getKrFisher(matrixInputData)))
    

def getFuncError(matrixInputData,symbolsArgs,countArgs):
    strFuncError = ''
    for indexRow in range(0,len(matrixInputData)):
        strFuncError+="("
        for indexColumn in range(len(matrixInputData[indexRow]) - 1,-1,-1):
            if indexColumn == len(matrixInputData[indexRow]) - 1:
                strFuncError+=str(symbolsArgs[countArgs - indexColumn - 1])
            elif indexColumn == 0:
                strFuncError+='+' + str(symbolsArgs[countArgs - indexColumn - 1]) + '*' + matrixInputData[indexRow][len(matrixInputData[indexRow]) - 1] + '-' + matrixInputData[indexRow][indexColumn]
            else:
                strFuncError+='+' + str(symbolsArgs[countArgs - indexColumn - 1]) + '*' + matrixInputData[indexRow][indexColumn]
        strFuncError+=")**2"
        if indexRow + 1 != len(matrixInputData):
            strFuncError+="+"
    return strFuncError


def getGradFunc(strFunc,symbolsArgs):
    countArgs = len(symbolsArgs)
    grad = []
    for indexArg in range(0,countArgs):
        grad.append(diff(strFunc,symbolsArgs[indexArg]))
    return grad


def getFuncForSigma(funcError):
    funcForSigma = funcError.replace('**2','')
    funcForSigma = funcForSigma.split(')+(')
    funcForSigma[0] = funcForSigma[0].replace('(','')
    funcForSigma[len(funcForSigma) - 1] = funcForSigma[len(funcForSigma) - 1].replace(')','')
    return funcForSigma


def getKrFisher(matrixInputData):
    countRows = len(matrixInputData)
    krFisher = 0
    sumY = 0
    sumY_2=0
    for i in range(0,countRows):
        sumY+=int(matrixInputData[i][0])
        sumY_2+=(int(matrixInputData[i][0])) ** 2 
    symY = sumY ** 2
    krFisher = (sumY_2 - sumY / countRows) / (countRows - 1)
    return krFisher
    

main()