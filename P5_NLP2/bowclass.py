# -*- coding: utf-8 -*-

import string
import heapq
from os import listdir

def main():
    print "### Start of Execution ###\n"

    #NSize es el numero de features.
    NSize = 400

    #Creamos un bag Of Words como un diccionario donde almacenaremos las palabras del dataset y su ocurrencia.
    bagOfWords = {}

    #Primero listamos los ficheros del dataset.
    fileList = listdir("dataset")
    replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

    #Para cada fichero del dataset...
    for fileName in fileList:
        filePath = "dataset/" + fileName
        textFile = openFile(filePath, 'r')

        for line in textFile:
            #Para cada linia nos quitamos de encima los signos de puntuación que son reemplazados por espacios.
            newLine = line.translate(replace_punctuation)
            #Para cada linia también pasamos todas las mayusculas a minusculas.
            newLine = newLine.lower()

            #Para cada palabra de cada linia...
            for word in newLine.split():

                #Si ya se encuentra en el diccionario, añadimos 1 a su valor.
                if word in bagOfWords:
                    bagOfWords[word] += 1.0
                #Si no se encuentra en el diccionario, se añade con valor 1.
                else:
                    bagOfWords[word] = 1.0


    #writeDicToFile('testOutput',bagOfWords)

    #Obtenemos las NSize palabras con mayor frecuencia del bag of words.
    largestKeys = heapq.nlargest(NSize, bagOfWords, key=bagOfWords.get)

    #print 'LargestKeys', largestKeys

    #Para cada documento del dataset creamos un diccionario, cada uno será un vector de features.
    textWordsDictionaries = [{} for x in range(len(fileList))]

    #print 'Calculating vectors:

    for textWordDictionary in textWordsDictionaries:
        # Para cada diccionario añadimos una key de label, con de momento el valor 'unlabeled'.
        textWordDictionary['#label'] = 'unlabeled'

        # Para cada diccionario añadimos una key para cada palabra de las NSize más frecuente.
        # con de momento el valor '0.0'.
        for key in largestKeys:
            textWordDictionary[key] = 0.0

    #Iteramos en cada fichero y diccionario a la vez.
    iter = 0
    for fileName in fileList:
        filePath = "dataset/" + fileName
        textFile = openFile(filePath, 'r')

        # Obtenemos el label del fichero, en este caso "male" o "female".
        label = fileName.split('_')[1]
        # Assignamos al diccionario de ese fichero el valor del label.
        textWordsDictionaries[iter]['#label'] = label
        # Para cada diccionario añadimos una key para nWords que representa el numero total de palabras de su texto.
        textWordsDictionaries[iter]['#nWords'] = 0.0

        #print 'Label', label

        # Volvemos a recorrer todas las palabras del fichero.
        for line in textFile:
            newLine = line.translate(replace_punctuation)
            newLine = newLine.lower()

            for word in newLine.split():
                # Para cada palabra actualizamos el valor de #nWords del diccionario del texto.
                textWordsDictionaries[iter]['#nWords'] += 1.0
                # Si la palabra se encuentra en las keys del diccionario, donde solo tenemos las
                # NSize palabras mas frecuentes del dataset, actualizamos su valor.
                if word in textWordsDictionaries[iter]:
                    textWordsDictionaries[iter][word] += 1.0

        # Para cada palabra del diccionario, le asignamos su ocurrencia en porcentaje.
        for key in textWordsDictionaries[iter].keys():
            nWords = textWordsDictionaries[iter]['#nWords']

            #Como se aprovecha el diccionario para almacenar otros datos, los filtramos.
            if key != '#label' and key != '#nWords':
                keyValue = textWordsDictionaries[iter][key]
                textWordsDictionaries[iter][key] = round((keyValue / nWords) * 100, 2)
        iter += 1

    #Podemos generar archivos de texto para hacer "debug" de los datos almacenados en los diccionarios.
    #writeDicToFile(str(0) + "_demoDict.txt", textWordsDictionaries[0])

    #Finalmente generamos el archivo Arff para Weka mediante la lista de diccionarios (o lista de vectores)
    writeDicListToArff("arffTest", textWordsDictionaries)


def openFile(fileName, option):
    print "- Opening", fileName, "to", option
    fileID = open(fileName, option)
    return fileID

def writeDicToFile(fileName, dict):

    print "\n## Writing dictionary to File", fileName, "..."

    file = openFile(fileName, 'w')

    for key in dict.keys():
        count = dict[key]

        key = key.replace("\r\n", "")
        newLine = key + "\t" + str(count) + "\n"
        file.write(newLine)

def writeDicListToArff(fileName, dictList):

    print "\n## Writing dictionary vector list to Arff File", fileName, "..."

    file = openFile(fileName + '.arff', 'w')

    # Titulo y Relation
    file.write("% 1. Title: Gender Text Database \n"
               "@RELATION genderText\n\n")

    # Para cada key del diccionario ( o posible feature )...
    for key in dictList[0].keys():
        # Si y solo si es una feature...
        if key != '#label' and key != '#nWords':
            # Printamos linia a linia el atributo, su nombre y tipo...
            line = "@ATTRIBUTE\t" + key + "\tNUMERIC\n"
            file.write(line)

    # Printamos el atributo de labels, en este caso "male" o "female".
    file.write("@ATTRIBUTE\tgender\t{male,female}\n")

    # Printamos los vectores de features.
    file.write("\n@DATA\n")
    for dict in dictList:
        line = ''
        for key in dict.keys():
            if key != '#label' and key != '#nWords':
                line = line + str(dict[key]) + ','
        line = line + dict['#label'] + '\n'
        file.write(line)


def endOfExecution():
    print "\n### End of Execution ### \n\n"

if __name__ == "__main__":
    main()
    endOfExecution()
