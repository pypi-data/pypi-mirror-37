import warnings

import numpy as np
import pandas as pd

from sm2.iolib.table import (SimpleTable,
                             default_txt_fmt,
                             default_latex_fmt,
                             default_html_fmt)

from sm2.regression.linear_model import OLS

ltx_fmt1 = default_latex_fmt.copy()
html_fmt1 = default_html_fmt.copy()


class TestSimpleTable(object):
    def test_SimpleTable_1(self):
        # Basic test, test_SimpleTable_1
        desired = """
=====================
      header1 header2
---------------------
stub1 1.30312 2.73999
stub2 1.95038 2.65765
---------------------
"""
        test1data = [[1.30312, 2.73999], [1.95038, 2.65765]]
        test1stubs = ('stub1', 'stub2')
        test1header = ('header1', 'header2')
        actual = SimpleTable(test1data, test1header, test1stubs,
                             txt_fmt=default_txt_fmt)
        actual = '\n%s\n' % actual.as_text()
        assert str(actual) == desired

    def test_SimpleTable_2(self):
        #  Test SimpleTable.extend_right()
        desired = """
=============================================================
           header s1 header d1            header s2 header d2
-------------------------------------------------------------
stub R1 C1  10.30312  10.73999 stub R1 C2  50.95038  50.65765
stub R2 C1  90.30312  90.73999 stub R2 C2  40.95038  40.65765
-------------------------------------------------------------
"""
        data1 = [[10.30312, 10.73999], [90.30312, 90.73999]]
        data2 = [[50.95038, 50.65765], [40.95038, 40.65765]]
        stubs1 = ['stub R1 C1', 'stub R2 C1']
        stubs2 = ['stub R1 C2', 'stub R2 C2']
        header1 = ['header s1', 'header d1']
        header2 = ['header s2', 'header d2']
        actual1 = SimpleTable(data1, header1, stubs1, txt_fmt=default_txt_fmt)
        actual2 = SimpleTable(data2, header2, stubs2, txt_fmt=default_txt_fmt)
        actual1.extend_right(actual2)
        actual = '\n%s\n' % actual1.as_text()
        assert str(actual) == desired

    def test_SimpleTable_3(self):
        # Test SimpleTable.extend() as in extend down
        desired = """
==============================
           header s1 header d1
------------------------------
stub R1 C1  10.30312  10.73999
stub R2 C1  90.30312  90.73999
           header s2 header d2
------------------------------
stub R1 C2  50.95038  50.65765
stub R2 C2  40.95038  40.65765
------------------------------
"""
        data1 = [[10.30312, 10.73999], [90.30312, 90.73999]]
        data2 = [[50.95038, 50.65765], [40.95038, 40.65765]]
        stubs1 = ['stub R1 C1', 'stub R2 C1']
        stubs2 = ['stub R1 C2', 'stub R2 C2']
        header1 = ['header s1', 'header d1']
        header2 = ['header s2', 'header d2']
        actual1 = SimpleTable(data1, header1, stubs1, txt_fmt=default_txt_fmt)
        actual2 = SimpleTable(data2, header2, stubs2, txt_fmt=default_txt_fmt)
        actual1.extend(actual2)
        actual = '\n%s\n' % actual1.as_text()
        assert str(actual) == desired

    def test_SimpleTable_4(self):
        # Basic test, test_SimpleTable_4 test uses custom txt_fmt
        txt_fmt1 = dict(data_fmts=['%3.2f', '%d'],
                        empty_cell=' ',
                        colwidths=1,
                        colsep=' * ',
                        row_pre='* ',
                        row_post=' *',
                        table_dec_above='*',
                        table_dec_below='*',
                        header_dec_below='*',
                        header_fmt='%s',
                        stub_fmt='%s',
                        title_align='r',
                        header_align='r',
                        data_aligns="r",
                        stubs_align="l",
                        fmt='txt')
        ltx_fmt1 = default_latex_fmt.copy()
        html_fmt1 = default_html_fmt.copy()
        cell0data = 0.0000
        cell1data = 1
        row0data = [cell0data, cell1data]
        row1data = [2, 3.333]
        table1data = [row0data, row1data]
        test1stubs = ('stub1', 'stub2')
        test1header = ('header1', 'header2')
        tbl = SimpleTable(table1data, test1header, test1stubs,
                          txt_fmt=txt_fmt1, ltx_fmt=ltx_fmt1,
                          html_fmt=html_fmt1)

        def test_txt_fmt1(self):
            # Limited test of custom txt_fmt
            desired = """
*****************************
*       * header1 * header2 *
*****************************
* stub1 *    0.00 *       1 *
* stub2 *    2.00 *       3 *
*****************************
"""
            actual = '\n%s\n' % tbl.as_text()
            assert actual == desired

        def test_ltx_fmt1(self):
            # Limited test of custom ltx_fmt
            desired = r"""
\begin{tabular}{lcc}
\toprule
               & \textbf{header1} & \textbf{header2}  \\
\midrule
\textbf{stub1} &       0.0        &        1          \\
\textbf{stub2} &        2         &      3.333        \\
\bottomrule
\end{tabular}
"""
            actual = '\n%s\n' % tbl.as_latex_tabular(center=False)
            assert actual == desired
            # Test "center=True" (the default):
            desired_centered = r"""
\begin{center}
%s
\end{center}
""" % desired[1:-1]
            actual_centered = '\n%s\n' % tbl.as_latex_tabular()
            assert actual_centered == desired_centered

        def test_html_fmt1(self):
            # Limited test of custom html_fmt
            desired = """
<table class="simpletable">
<tr>
    <td></td>    <th>header1</th> <th>header2</th>
</tr>
<tr>
  <th>stub1</th>   <td>0.0</td>      <td>1</td>
</tr>
<tr>
  <th>stub2</th>    <td>2</td>     <td>3.333</td>
</tr>
</table>
"""
            actual = '\n%s\n' % tbl.as_html()
            # trim trailing whitespace for comparison
            actual = '\n'.join((line.rstrip() for line in actual.split('\n')))
            assert actual == desired

        test_txt_fmt1(self)
        test_ltx_fmt1(self)
        test_html_fmt1(self)

    def test_SimpleTable_special_chars(self):
        # Simple table with characters: (%, >, |, _, $, &, #)
        cell0c_data = 22
        cell1c_data = 1053
        row0c_data = [cell0c_data, cell1c_data]
        row1c_data = [23, 6250.4]
        table1c_data = [row0c_data, row1c_data]
        test1c_stubs = ('>stub1%', 'stub_2')
        test1c_header = ('#header1$', 'header&|')
        tbl_c = SimpleTable(table1c_data, test1c_header, test1c_stubs,
                            ltx_fmt=ltx_fmt1)

        def test_ltx_special_chars(self):
            # Test for special characters (latex) in headers and stubs
            desired = r"""
\begin{tabular}{lcc}
\toprule
                    & \textbf{\#header1\$} & \textbf{header\&$|$}  \\
\midrule
\textbf{$>$stub1\%} &          22          &         1053          \\
\textbf{stub\_2}    &          23          &        6250.4         \\
\bottomrule
\end{tabular}
"""
            actual = '\n%s\n' % tbl_c.as_latex_tabular(center=False)
            assert actual == desired
        test_ltx_special_chars(self)
        # WTF Is this supposed to be a nested test or what?

    def test_regression_with_tuples(self):
        i = pd.Series([1, 2, 3, 4] * 10, name="i")
        y = pd.Series([1, 2, 3, 4, 5] * 8, name="y")
        x = pd.Series([1, 2, 3, 4, 5, 6, 7, 8] * 5, name="x")

        df = pd.DataFrame(index=i.index)
        df = df.join(i)
        endo = df.join(y)
        exo = df.join(x)
        endo_groups = endo.groupby("i")
        exo_groups = exo.groupby("i")
        exo_Df = exo_groups.agg([np.sum, np.max])
        endo_Df = endo_groups.agg([np.sum, np.max])
        reg = OLS(exo_Df[[("x", "sum")]], endo_Df).fit()
        interesting_lines = []

        with warnings.catch_warnings():
            # Catch ominormal warning, not interesting here
            warnings.simplefilter("ignore")
            for line in str(reg.summary()).splitlines():
                if "('" in line:
                    interesting_lines.append(line[:38])

        desired = ["Dep. Variable:           ('x', 'sum') ",
                   "('y', 'sum')      1.4595      0.209   ",
                   "('y', 'amax')     0.2432      0.035   "]

        assert sorted(desired) == sorted(interesting_lines)
