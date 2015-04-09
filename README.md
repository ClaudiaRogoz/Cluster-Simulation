# Cluster-Simulation
Claudia Rogoz
331CA

Tema 1 ASC

Tema a constat in simularea unui cluster. 
Pentru aceasta, m-am folosit de scheletul de cod;
In implementare m-am folosit de urmatoarele fisiere: node.py, cond_barrier.py, worker.py

Clasa Node simuleaza un nod in cluster;
Constructorul lui Node  va initia 16 threaduri(workeri), care vor rula asa cum este precizat si in enunt,
pana cand este apelata metoda shutdown()
Clasa se foloseste de o copie a listei data; aceasta copie numita "copy" va fi folosita in cadrul etapei
scatter; pentru sincronizarea datelor, in momentul in care se incheie o runda, prin apelarea metodei 
sync_results(), se foloseste o bariera comuna tuturor nodurilor clusterului; astefel, in urma acestei bariere
fiecare nod isi actualizeaza data cu valorile din bufferul "copy";
In omentul in care se apeleaza metoda shutdown, se trimit niste pseudo-taskuri ( in numar de 16 == numarul de 
threaduri in fiecare nod) care vor determina terminarea threadurilor.

In node m-am folosit de un lock mutex folosit de 2 elemente de sincronizare-condition. Un condition (condition) 
se foloseste in momentul in care se scot, respectiv se adauga taskuri pentru procesare in lista thread_pool. 
Un alt condition(all_tasks_done) etse folosit pentru blocarea lui sync_results pana cand toate taskurile din runda
curenta au fost procesate.Variabila de care se foloseste este "unfinished_tasks" care numara cate taskuri mai 
sunt de procesat.

Implementarea propriu-zisa este bazata pe algoritmul producatori-consumatori. In cazul de fata Nodul este
producatorul  (Nodul prin intermediul metodelor sale apelate), iar consumatorii sunt cele 16 threaduri.
Consumatorii (threadurile == workerii) se blocheaza pana cand au de rezolvat un task; In momentul in care
un task a aparut se deblocheaza un task si incepe sa-l proceseze; Se verifica apoi conditia ca taskul sa
nu fie unul "fals". Daca este, atunci threadul isi incheie exxecutia. Altfel, se face gather pe baza 
listei in_slices, rezultand o lista "res". Dupa aceasta etapa se executa task.run(res). in cele din 
urma, se face scatter in bufferul "copy". Dupa ce s-a incheiat runda, se asteapta rezolvarea tuturor tasurilor
din lista thread_pool, urmand apoi o bariera intre toate nodurile clusterului. 	In final se updateaza data
cu valorile din copy. Se pune din nou o bariera pentru a fi siguri ca toate nodurile si-au updatat valorile.
Algoritmul se repeta apoi pana la shutdown.


------------------Rezultate qsub -q ibm-nehalem.q -b y ./run_tests.she ------------------------------



**************** Start Test 1 *****************
Errors in iteration 1 of 1:
No errors
***************** End Test 1 ******************

**************** Start Test 2 *****************
Errors in iteration 1 of 20:
No errors
Errors in iteration 2 of 20:
No errors
Errors in iteration 3 of 20:
No errors
Errors in iteration 4 of 20:
No errors
Errors in iteration 5 of 20:
No errors
Errors in iteration 6 of 20:
No errors
Errors in iteration 7 of 20:
No errors
Errors in iteration 8 of 20:
No errors
Errors in iteration 9 of 20:
No errors
Errors in iteration 10 of 20:
No errors
Errors in iteration 11 of 20:
No errors
Errors in iteration 12 of 20:
No errors
Errors in iteration 13 of 20:
No errors
Errors in iteration 14 of 20:
No errors
Errors in iteration 15 of 20:
No errors
Errors in iteration 16 of 20:
No errors
Errors in iteration 17 of 20:
No errors
Errors in iteration 18 of 20:
No errors
Errors in iteration 19 of 20:
No errors
Errors in iteration 20 of 20:
No errors
***************** End Test 2 ******************

**************** Start Test 3 *****************
Errors in iteration 1 of 4:
No errors
Errors in iteration 2 of 4:
No errors
Errors in iteration 3 of 4:
No errors
Errors in iteration 4 of 4:
No errors
***************** End Test 3 ******************

**************** Start Test 4 *****************
Errors in iteration 1 of 4:
No errors
Errors in iteration 2 of 4:
No errors
Errors in iteration 3 of 4:
No errors
Errors in iteration 4 of 4:
No errors
***************** End Test 4 ******************

**************** Start Test 5 *****************
Errors in iteration 1 of 10:
No errors
Errors in iteration 2 of 10:
No errors
Errors in iteration 3 of 10:
No errors
Errors in iteration 4 of 10:
No errors
Errors in iteration 5 of 10:
No errors
Errors in iteration 6 of 10:
No errors
Errors in iteration 7 of 10:
No errors
Errors in iteration 8 of 10:
No errors
Errors in iteration 9 of 10:
No errors
Errors in iteration 10 of 10:
No errors
***************** End Test 5 ******************

**************** Start Test 6 *****************
Errors in iteration 1 of 10:
No errors
Errors in iteration 2 of 10:
No errors
Errors in iteration 3 of 10:
No errors
Errors in iteration 4 of 10:
No errors
Errors in iteration 5 of 10:
No errors
Errors in iteration 6 of 10:
No errors
Errors in iteration 7 of 10:
No errors
Errors in iteration 8 of 10:
No errors
Errors in iteration 9 of 10:
No errors
Errors in iteration 10 of 10:
No errors
***************** End Test 6 ******************

**************** Start Test 7 *****************
Errors in iteration 1 of 1:
No errors
***************** End Test 7 ******************

**************** Start Test 8 *****************
Errors in iteration 1 of 1:
No errors
***************** End Test 8 ******************

**************** Start Test 9 *****************
Errors in iteration 1 of 2:
No errors
Errors in iteration 2 of 2:
No errors
***************** End Test 9 ******************

**************** Start Test 10 *****************
Errors in iteration 1 of 1:
No errors
***************** End Test 10 ******************


-----------------------------------------------------------------------

Test Test 1     Finished...............100% completed
Test Test 2     Finished...............100% completed
Test Test 3     Finished...............100% completed
Test Test 4     Finished...............100% completed
Test Test 5     Finished...............100% completed
Test Test 6     Finished...............100% completed
Test Test 7     Finished...............100% completed
Test Test 8     Finished...............100% completed
Test Test 9     Finished...............100% completed
Test Test 10    Finished...............100% completed
