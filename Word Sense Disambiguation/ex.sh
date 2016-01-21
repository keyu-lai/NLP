time python main.py data/English-train.xml data/English-dev.xml KNN-English.answer SVM-English.answer Best-English.answer English

./scorer2 KNN-English.answer data/English-dev.key data/English.sensemap
./scorer2 SVM-English.answer data/English-dev.key data/English.sensemap
./scorer2 Best-English.answer data/English-dev.key data/English.sensemap

time python main.py data/Spanish-train.xml data/Spanish-dev.xml KNN-Spanish.answer SVM-Spanish.answer Best-Spanish.answer Spanish

./scorer2 KNN-Spanish.answer data/Spanish-dev.key
./scorer2 SVM-Spanish.answer data/Spanish-dev.key
./scorer2 Best-Spanish.answer data/Spanish-dev.key

time python main.py data/Catalan-train.xml data/Catalan-dev.xml KNN-Catalan.answer SVM-Catalan.answer Best-Catalan.answer Catalan

./scorer2 KNN-Catalan.answer data/Catalan-dev.key
./scorer2 SVM-Catalan.answer data/Catalan-dev.key
./scorer2 Best-Catalan.answer data/Catalan-dev.key
