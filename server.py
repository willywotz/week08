from flask import Flask, flash, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = b'fkdkfdkdiekdk'

my_contacts = [
    {'id': '65122420118', 'name': 'นายสุเมธ ตังคณิตานนท์', 'mobile': '062-145-6455'},
    {'id': '64122420116', 'name': 'นายพรวิเชียร ภัสร์ปรพงษ์', 'mobile': '083-683-6245'},
    {'id': '64122420223', 'name': 'นายรัชชานนท์ วงศ์กลม', 'mobile': '097-009-3297'},
    {'id': '65122040331', 'name': 'นางสาวอรสุดา ไชยพรม', 'mobile': '096-420-3218'},
    {'id': '65122710115', 'name': 'นายวิษณุ วงศ์สวัสดิ์', 'mobile': '084-585-0770'},
    {'id': '64122420130', 'name': 'นางสาวสุชัญญา หวังดี', 'mobile': '063-857-5607'},
]

@app.route('/')
def index():
    flash('this is flash message send from server', 'info')
    return render_template('index.html', title='Home Page')

@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    tmp_contacts = []
    name = None
    if request.method == 'GET':
        tmp_contacts.extend(my_contacts)
    else:
        name = request.form['name']
        for contact in my_contacts:
            if contact['name'].find(name) > -1:
                tmp_contacts.append(contact)
    return render_template('contact/index.html', title='My Contacts', contacts=tmp_contacts, name=name)

@app.route('/new_contact', methods=['POST', 'GET'])
def new_contact():
    if request.method == 'POST':
        contact = {}
        contact['id'] = request.form.get('id', '')
        contact['name'] = request.form.get('name', '')
        contact['mobile'] = request.form.get('mobile', '')
        c_id_check = contact['id'] == ''
        for c in my_contacts:
            if c['id'] == contact['id']:
                c_id_check = True
                break
        if c_id_check == True:
            flash('contact id can not blank or duplicate', 'danger')
            return redirect(url_for('contacts'))
        my_contacts.append(contact)
        flash('contact added', 'success')
        return redirect(url_for('contacts'))
        
    return render_template('contact/new_contact.html', title='New Contact')

@app.route('/edit_contact', methods=['POST', 'GET'])
def edit_contact():
    target_contact = None
    if request.method == 'GET':
        contact_id = request.args.get('id', None)
        for c in my_contacts:
            if c['id'] == contact_id:
                target_contact = c
                break
        if target_contact == None:
            flash('contact not found', 'warning')
            return redirect(url_for('contacts'))
    if request.method == 'POST':
        old_contact_id = request.form.get('old_contact_id', None)
        for c in my_contacts:
            if c['id'] == old_contact_id:
                target_contact = c
                break
        target_contact['id'] = old_contact_id
        target_contact['name'] = request.form.get('name', '')
        target_contact['mobile'] = request.form.get('mobile', '')
        flash('contact updated', 'success')
        return redirect(url_for('contacts'))

    return render_template('contact/edit_contact.html', title='Edit Contact', contact=target_contact)

@app.route('/delete_contact')
def delete_contact():
    contact_id = request.args.get('id', None)
    target_contact = None
    if contact_id != None:
        for contact in my_contacts:
            if contact['id'] == contact_id:
                target_contact = contact
                break
    if target_contact == None:
        flash('contact not found', 'warning')
    else:
        my_contacts.remove(target_contact)
        flash('contact removed', 'success')
    return redirect(url_for('contacts'))