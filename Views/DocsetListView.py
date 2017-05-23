from Utilities import UISearchBarWrapper
import ui

tv = ui.TableView()
class DocsetListView (object):
	def __init__(self, docsets, cheatsheets, usercontributed, docset_selected_callback, cheatsheet_selected_callback, usercontributed_selected_callback):
		self.keepDocsets = docsets
		self.docsets = docsets
		self.keepCheatsheets = cheatsheets
		self.cheatsheets = cheatsheets
		self.keepUsercontributed = usercontributed
		self.usercontributed = usercontributed
		self.docset_selected_callback = docset_selected_callback
		self.cheatsheet_selected_callback = cheatsheet_selected_callback
		self.usercontributed_selected_callback = usercontributed_selected_callback
		self.docsetSection = -1
		self.cheatsheetSection = -1
		self.usercontributedSection = -1
		self.numberOfSections = 0
		self.searchText = ''
	
		
	def tableview_did_select(self, tableview, section, row):
		if section == self.docsetSection:
			self.docset_selected_callback(self.docsets[row])
		elif section == self.cheatsheetSection:
			self.cheatsheet_selected_callback(self.cheatsheets[row])
		elif section == self.usercontributedSection:
			self.usercontributed_selected_callback(self.usercontributed[row])
	
	def tableview_title_for_header(self, tableview, section):
		if section == self.docsetSection:
			return 'Docsets'
		elif section == self.cheatsheetSection:
			return 'Cheat Sheets'
		elif section == self.usercontributedSection:
			return 'User Contributed Docsets'	
	
	def tableview_number_of_sections(self, tableview):
		self.determineSections()
		return self.numberOfSections
		
	def tableview_number_of_rows(self, tableview, section):
		if section == self.docsetSection:
			return len(self.docsets)
		elif section == self.cheatsheetSection:
			return len(self.cheatsheets)
		elif  section == self.usercontributedSection:
			return len(self.usercontributed)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		if section == self.docsetSection:
			cell.text_label.text = self.docsets[row]['name']
			cell.accessory_type = 'disclosure_indicator'
			if not self.docsets[row]['image'] == None:
				cell.image_view.image = self.docsets[row]['image']
		elif section == self.cheatsheetSection:
			cell.text_label.text = self.cheatsheets[row].name
			cell.accessory_type = 'disclosure_indicator'
			if not self.cheatsheets[row].image == None:
				cell.image_view.image = self.cheatsheets[row].image
		elif section == self.usercontributedSection:
			cell.text_label.text = self.usercontributed[row].name
			cell.detail_text_label.text = 'Contributed by ' + self.usercontributed[row].authorName
			cell.accessory_type = 'disclosure_indicator'
			if not self.usercontributed[row].image == None:
				cell.image_view.image = self.usercontributed[row].image
		return cell
	
	def determineSections(self):
		self.numberOfSections = 0
		if len(self.docsets) > 0:
			self.docsetSection = self.numberOfSections
			self.numberOfSections = self.numberOfSections + 1
		else:
			self.docsetSection = -1
		if len(self.cheatsheets) > 0:
			self.cheatsheetSection = self.numberOfSections
			self.numberOfSections = self.numberOfSections + 1
		else:
			self.cheatsheetSection = -1
		if len(self.usercontributed) > 0:
			self.usercontributedSection = self.numberOfSections
			self.numberOfSections = self.numberOfSections + 1
		else:
			self.usercontributedSection = -1
	
	def filterData(self, text):
		self.searchText = text
		if text == '':
			self.docsets = self.keepDocsets
			self.cheatsheets = self.keepCheatsheets
			self.usercontributed = self.keepUsercontributed
		else:
			doc = []
			for d in self.keepDocsets:
				if(d['name'].lower().find(str(text).lower())>-1):
					doc.append(d)
			self.docsets = doc
			che = []
			for c in self.keepCheatsheets:
				if(c.name.lower().find(str(text).lower())>-1):
					che.append(c)
			self.cheatsheets = che
			use = []
			for u in self.keepUsercontributed:
				if(u.name.lower().find(str(text).lower())>-1):
					use.append(u)
			self.usercontributed = use
		tv.reload()

def get_view(docsets, cheatsheets, usercontributed, docset_selected_callback, cheatsheet_selected_callback, usercontrobuted_selected_callback):
	tv.flex = 'WH'
	tv.name = 'PyDoc'
	data = DocsetListView(docsets, cheatsheets, usercontributed, docset_selected_callback, cheatsheet_selected_callback, usercontrobuted_selected_callback)
	tv.delegate = data
	tv.data_source = data
	v = UISearchBarWrapper.get_view(tv, data.filterData)
	return v

def refresh_view(docsets, cheatsheets, usercontributed):
	#tv.data_source.docsets = docsets
	tv.data_source.keepDocsets = docsets
	#tv.data_source.cheatsheets = cheatsheets
	tv.data_source.keepCheatsheets = cheatsheets
	#tv.data_source.usercontributed = usercontributed
	tv.data_source.keepUsercontributed = usercontributed
	tv.data_source.filterData(tv.data_source.searchText)
	tv.reload_data()
	tv.reload()
	
