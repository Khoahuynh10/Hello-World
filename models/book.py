
from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _log_access = True

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    published_date = fields.Date(string="Published Date")
    description = fields.Text(string="Description")
    cover = fields.Binary(string="Cover Image")
    state = fields.Selection([
        ('available', 'Đang rảnh'),
        ('borrowed', 'Đang được mượn'),]
    , string="Đang rảnh")
    
    borrower_id = fields.Many2one(
        'res.users',
        string="Người mượn"
    )
    borrowed_date = fields.Datetime(string="Borrowed Date", readonly=True)

    def write(self, vals):
        if self.env.user.has_group('library.group_library_editor'):
            allowed_fields = ['borrower_id']
            for field in vals:
                if field not in allowed_fields:
                    raise AccessError("You can only edit borrower.")
        return super().write(vals)


    @api.onchange('borrower_id')
    def _onchange_borrower_id(self):
        """ Tự động set ngày mượn khi assign borrower """
        if self.borrower_id:
            self.state = 'borrowed'
            if not self.borrowed_date:
                self.borrowed_date = fields.Datetime.now()
        else:
            self.state = 'available'
            self.borrowed_date = False

