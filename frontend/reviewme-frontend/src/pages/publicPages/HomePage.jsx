import React from "react";
import CenterBody from "../../layouts/CenterBody";
import useReviews from "../../hooks/useReviews";
import ReviewsList from "../../components/lists/ReviewsList";

function HomePage() {
  return (
    <CenterBody>
      <p> Welcome To Home </p>
      <ReviewsList />
    </CenterBody>
  );
}
export default HomePage;
