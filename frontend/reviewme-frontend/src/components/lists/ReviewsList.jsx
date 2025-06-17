import React from "react";
import useReviews from "../../hooks/useReviews";
import Review from "../objects/Review";

function ReviewsList() {
  const { reviews, loading, error, pageInfo, refetch } = useReviews(1, 10);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="reviews-list">
      {reviews.map((review) => (
        <Review review={review} key={review.id} />
      ))}
    </div>
  );
}

export default ReviewsList;
