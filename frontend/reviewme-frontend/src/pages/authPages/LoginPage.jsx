import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";
import AuthLayout from "../../layouts/AuthLayout";
import { useAuth } from "../../context/AuthContext";

function LoginPage() {
  const { loginUser } = useAuth();
  const handleSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    loginUser({
      email: data.get("email"),
      password: data.get("password"),
    });
    form.reset();
  };
  return (
    <AuthLayout>
      <h1 className="form-title">Log In</h1>
      <p className="form-subtitle">
        <strong>Welcome Back!</strong> Please log in to continue.
      </p>
      <Form onSubmit={handleSubmit}>
        {/* <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
      </Form.Group> */}

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" name="email" placeholder="Enter Email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            name="password"
            placeholder="Password"
          />
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
