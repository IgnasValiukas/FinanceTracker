Finance Tracker is a Django-based web application that helps users manage their personal finances by logging and tracking transactions.

**Key Features**
1. User Account:
   - Register a new account
   - Log in to access your data
   - Reset password via email if forgotten
2. Add Transactions:
   - Enter the amount
   - Choose type: Income or Expense
   - Write a custom title
   - Select a category
   - Set the transaction date
   - Optionally add a description for more context
3. View All Transactions:
   - See a complete list of your financial activity in one place
   - See each transaction detail info
4. Track Balance:
   - View your current profile balance based on income and expenses
5. Manage Profile:
   - Edit your username and profile image
6. Update Transactions:
   - Edit or delete any of your past transactions

❗️⚙️**Setup Guide**  
Make sure Python and pip are installed, then run:
1. pip install django
2. pip install pillow
3. pip install django-tinymce
4. pip install crispy-bootstrap4
5. pip install django-crispy-forms
6. pip install django-widget-tweaks

▶️**Run the Server:**  
python manage.py runserver

💡 **Recommended Run Configuration (Optional)**  
To streamline server startup in your IDE:
1. Click the three dots near the Run button
2. Select Edit...
3. When window opens, Click the + icon and choose Python
4. Name it something like 'run_server'
5. Set the Script path to your project's manage.py
6. In Script parameters, add: runserver
7. Click Apply, then OK
