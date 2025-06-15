import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import AuthLayout from "../../layouts/AuthLayout";

function LoginPage() {
  return (
    <AuthLayout>
      <h1 className="form-title">Log In</h1>
      <p className="form-subtitle">
        <strong>Welcome Back!</strong> Please log in to continue.
      </p>
      <Form>
        {/* <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
      </Form.Group> */}

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control type="text" placeholder="Enter username" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" />
        </Form.Group>

        {/* <Form.Group className="mb-3" controlId="formBasicCheckbox">
        <Form.Check type="checkbox" label="Check me out" />
      </Form.Group> */}

        <Button className="form-button" type="submit">
          Log In
        </Button>
      </Form>
    </AuthLayout>
  );
}

export default LoginPage;
