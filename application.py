from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ic_database_setup import Base, User, Category, Item

app = Flask(__name__)


engine = create_engine('sqlite:///itemcategory.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/<int:category_id>/')
def categoryList(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('ic_menu.html', category=category, items=items)


@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST': # executed when POST is performed
        newItem = Item(
            name=request.form['name'], category_id=category_id)
        app.logger.debug("output: " + str(category_id))
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryList'), category_id=category_id)
    else: # executed when GET is performed
        return render_template('ic_new_item.html', category_id=category_id)


@app.route('/categories/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('categoryList'), category_id=category_id)
    else:
        return render_template('ic_edit_item.html',
                               category_id=category_id,
                               item_id=item_id,
                               item=editedItem)

@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('categoryList'), category_id=category_id)
    else:
        return render_template('ic_delete_item.html',
                               item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
