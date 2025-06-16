import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import AuthLayout from "../../layouts/AuthLayout";

function RegisterPage() {
  return (
    <AuthLayout>
      <h1 className="form-title">Register</h1>
      <p className="form-subtitle">
        <strong>Welcome!</strong> Please register to continue.
      </p>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control type="text" placeholder="Enter username" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" />
        </Form.Group>

        <Button className="form-button" type="submit">
          Create Account
        </Button>
      </Form>
    </AuthLayout>
  );
}

export default RegisterPage;
