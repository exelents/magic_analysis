# Magic analysis

Эта программа нужна для проведения научных опытов, а именно для сравнения выборок данных полученных с микроскопа. 

В данном случае идёт речь о живых тканях, и программа сравнивает выборки размеров составных частей клетки (цитоплазма, ядро, ядрышки).

При проведении опыта существует как минимум две выборки - опытная и контрольная. Для того чтоб сравнить эти данные их нужно загрузить в две разные подпапки в папку "input" рядом с исполняемым файлом программы.
Сами данные в выборках могут иметь папки с подвыборками, но структура выборок(опытной и контрольной) должны быть одинакова. 

Пример структуры данных в папке ***input***: 
- input
    - контрольная
        - подвыборка 1
            - данные.a.ods
            - данные.b.ods
            - данные.c.ods
            - данные.d.ods
        - подвыборка 2
            - данные.e.ods
            - данные.f.ods
        - подвыборка 3
            - данные.g.ods
    - опыт
        - подвыборка 1
            - данные.h.ods
            - данные.i.ods
            - данные.j.ods
            - данные.k.ods
        - подвыборка 2
            - данные.l.ods
            - данные.m.ods
        - подвыборка 3
            - данные.n.ods
            
Как видно, структура дерева каталогов папок "контрольная" и "опыт" должна повторяться. Названия .ods файлов в конечных каталогах с выборками значения на имеют.


После отработки программы в папке ***output*** сформируется несколько файлов:
- report.docx  - файл с отчётом: графики, результаты тестов.
- report.docx.json то же самое, в формате json, для удобной обработи другой программой.
- errors.txt - журнал с сообщениями об ошибках в ходе работы.
- img - папка с картинками, графиками сгенерированными для отчёта. На неё ссылаются пути к графикам в .json отчёте (см. второй пункт списка). Для отчёта в формате Word (.docx) она не нужна.
- DATA_HIGHLIGHTS - папка хранит образ данных из папки ***input*** в которых в отдельных колонках подсвечены ошибочные значения в данных. Столбец ***chauvenet*** - это результат проверки на критерий Шовене среди данных одной подвыборки (подпапки) одного параметра (площадь цитоплазмы, ядра, ядрышка). Столбец data_structure - проверка логической структуры данных - программа полагает, что данные идут в порядке: цитоплазма - ядро - несколько ядрышек. Если структура не соблюдается - ошибка подсветится в этом поле. 


Алгоритм действий:
- создать папку ***input*** в каталоге с программой;
- сохранить сырые данные с микроскопа в формате ods в папку input;
- соблюсти одинаковую структуру выборок, как для контрольных, так и для опытных;
- запустить программу;
- получить отчёт по анализу и подсветку ошибок в данных из папки ***output***;

### Тестовые данные
- Данные не очищенные от ошибок, все тесты проходит только одна подвыборка: [data-with-errors.7z](data-with-errors.7z)


### TODO
- Выложить в доступ верифицированные тестовые данныеб проходящие все тесты;
- Do English translation of Readme.md

### Copyrights
This program is licensed under GNU General Public License,
see <https://www.gnu.org/licenses/>
