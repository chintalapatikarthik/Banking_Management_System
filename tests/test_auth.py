def test_login_page_renders(client):
    """Test that login page loads with HTTP 200."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Sign In to Dashboard" in response.data

def test_admin_login_success(client):
    """Test authenticating with default admin credentials."""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'Admin@123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Signed in as Admin" in response.data

def test_employee_login_success(client):
    """Test authenticating with default employee credentials."""
    response = client.post('/login', data={
        'username': 'employee',
        'password': 'Employee@123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Signed in as Employee" in response.data

def test_invalid_password_rejected(client):
    """Test that incorrect passwords are rejected."""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'WrongPassword999'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_logout(client):
    """Test signing out."""
    client.post('/login', data={'username': 'admin', 'password': 'Admin@123'})
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been successfully logged out" in response.data
