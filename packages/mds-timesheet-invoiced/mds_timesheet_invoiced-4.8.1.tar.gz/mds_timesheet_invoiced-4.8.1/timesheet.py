# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from sql.conditionals import Case
from sql.functions import Substring
from sql import Null
from trytond.transaction import Transaction
from trytond.pool import Pool


__all__ = ['TimesheetLine']

sel_invoiceinfo = [
        ('na', 'Not Invoiceable'),
        ('i', 'To Invoice'),
        ('d', 'Invoiced'),
    ]
    
    
class TimesheetLine(metaclass=PoolMeta):
    __name__ = 'timesheet.line'
    
    invoiceinfo = fields.Function(fields.Selection(string=u'Invoice info', 
        readonly=True, selection=sel_invoiceinfo), 
        'get_invoiceinfo', searcher='search_invoiceinfo')

    @classmethod
    def get_invoiceinfo_sql(cls):
        """ sql-code for query
        """
        pool = Pool()
        TimesheetLine = pool.get('timesheet.line')
        TimesheetWork = pool.get('timesheet.work')
        ProjectWork = pool.get('project.work')
        tab_tsl = TimesheetLine.__table__()
        tab_tsw = TimesheetWork.__table__()
        tab_pw = ProjectWork.__table__()
        tab_pw2 = ProjectWork.__table__()
        tab_pw3 = ProjectWork.__table__()
        tab_pw4 = ProjectWork.__table__()
        
        proj_work = 'project.work,'
        # get id_line and id_work
        tab_linework = tab_tsl.join(tab_tsw, condition=tab_tsw.id==tab_tsl.work
            ).select(tab_tsl.id.as_('id_line'),
                Case (
                    (Substring(tab_tsw.origin, 1, len(proj_work)) == proj_work, 
                        Substring(tab_tsw.origin, len(proj_work) + 1).cast('integer')
                    ),
                    else_ = None
                ).as_('id_work'),
                tab_tsl.invoice_line,
            )
        
        qu1 = tab_linework.join(tab_pw, condition=tab_pw.id==tab_linework.id_work
            ).join(tab_pw2,
                type_='LEFT OUTER',
                condition=(tab_pw.parent==tab_pw2.id) & 
                    ((tab_pw.type != 'project') | (tab_pw.project_invoice_method != 'timesheet'))
            ).join(tab_pw3,
                type_='LEFT OUTER',
                condition=(tab_pw2.parent==tab_pw3.id) &
                    ((tab_pw2.type != 'project') | (tab_pw2.project_invoice_method != 'timesheet'))
            ).join(tab_pw4,
                type_='LEFT OUTER',
                condition=(tab_pw3.parent==tab_pw4.id) &
                    ((tab_pw3.type != 'project') | (tab_pw3.project_invoice_method != 'timesheet'))
            ).select(tab_linework.id_line,
                tab_linework.invoice_line,
                tab_pw.type.as_('type1'),
                tab_pw.project_invoice_method.as_('meth1'),
                tab_pw2.type.as_('type2'),
                tab_pw2.project_invoice_method.as_('meth2'),
                tab_pw3.type.as_('type3'),
                tab_pw3.project_invoice_method.as_('meth3'),
                tab_pw4.type.as_('type4'),
                tab_pw4.project_invoice_method.as_('meth4'),
            )

        qu2 = qu1.select(qu1.id_line,
                Case(
                    (qu1.invoice_line != Null, 'd'),
                    ((qu1.type1 == 'project') & (qu1.meth1 == 'timesheet'), 'i'),
                    ((qu1.type2 == 'project') & (qu1.meth2 == 'timesheet'), 'i'),
                    ((qu1.type3 == 'project') & (qu1.meth3 == 'timesheet'), 'i'),
                    ((qu1.type4 == 'project') & (qu1.meth4 == 'timesheet'), 'i'),
                    else_ = 'na'
                ).as_('invoiceable')
            )
        return qu2
        
    @staticmethod
    def order_invoiceinfo(tables):
        tab_tsl, _ = tables[None]

        return [Case((tab_tsl.invoice_line == Null, 0), else_=1)]

    @classmethod
    def get_invoiceinfo(cls, lines, names):
        """ query table
        """
        id_lst = [x.id for x in lines]
        tab_qu = cls.get_invoiceinfo_sql()
        cursor = Transaction().connection.cursor()

        # prepare result
        res3 = {'invoiceinfo': {}}
        for i in id_lst:
            res3['invoiceinfo'][i] = 'na'
        
        qu1 = tab_qu.select(tab_qu.id_line,
                tab_qu.invoiceable,
                where=tab_qu.id_line.in_(id_lst)
            )
        cursor.execute(*qu1)
        l1 = cursor.fetchall()
        
        for i in l1:
            (id1, inf1) = i
            res3['invoiceinfo'][id1] = inf1

        res2 = {}
        for i in res3.keys():
            if i in names:
                res2[i] = res3[i]
        return res2

    @classmethod
    def search_invoiceinfo(cls, name, clause):
        """ sql-code for table search
        """
        tab_qu = cls.get_invoiceinfo_sql()
        Operator = fields.SQL_OPERATORS[clause[1]]
        
        qu1 = tab_qu.select(tab_qu.id_line,
                where=Operator(tab_qu.invoiceable, clause[2]),
            )
        return [('id', 'in', qu1)]

# end TimesheetLine
