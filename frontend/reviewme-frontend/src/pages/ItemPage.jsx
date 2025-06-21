import { useNavigate, useParams } from "react-router-dom";
import useItem from "../hooks/useItem";
import "../styles/ItemPage.css";
import { FaHashtag } from "react-icons/fa";
import ItemReviewsList from "../components/lists/ItemReviewsList";

import ItemsSkeleton from "../pages/stillPages/ItemsSkeleton";

const ItemPage = () => {
  const { id } = useParams();
  const { item, loading, error, reviews, pageInfo, refetch, setPage } =
    useItem(id);

  const navigate = useNavigate();

  // console.log(reviews);
  if (loading) {
    return (
      <div className="search-page">
        <div className="search-container">
          {Array.from({ length: 2 }).map((_, index) => (
            <ItemsSkeleton key={index} />
          ))}
        </div>
      </div>
    );
  }
  if (error) {
    // navigate("/NotFound", { state: { error } });
    return (
      <div className="item-page">
        <div className="item-container">Error: {error}</div>
      </div>
    );
  }
  if (!item) {
    navigate("/NotFound", { state: { error } });
    return (
      <div className="item-page">
        <div className="item-container">Item not found.</div>
      </div>
    );
  }

  return (
    <div className="item-page">
      <Item item={item} />
      <ItemReviewsList
        reviews={reviews}
        pageInfo={pageInfo}
        setPage={setPage}
        refetch={refetch}
        error={error}
        loading={loading}
      />
    </div>
  );
};

function Item({ item }) {
  return (
    <div className="item-container">
      <span className="item-title">{item.name}</span>
      <div className="item-meta">
        <span className="item-rating">
          ★ {item.average_rating} ({item.review_count} reviews)
        </span>
        {item.tags && item.tags.length > 0 && <Tags tags={item.tags} />}
      </div>
      <div className="item-details">
        <p className="item-description">{item.description}</p>
      </div>
      {item.links && item.links.length > 0 && <></>}
      {item.media && item.media.length > 0 && <ItemMedia media={item.media} />}
    </div>
  );
}

function Tags({ tags }) {
  return (
    <div className="item-tags">
      {tags.map((tag, i) => (
        <Tag key={i} tag={tag} />
      ))}
    </div>
  );
}

function Tag({ tag }) {
  const handleTagClick = () => {
    // navigate(`/tags/${tag}`);
    // console.log(`Tag clicked: ${tag}`);
  };
  return (
    <div className="item-tag" onClick={handleTagClick}>
      <FaHashtag size={10} className="tag-icon" />
      <span>{tag}</span>
    </div>
  );
}

function ItemMedia({ media }) {
  return (
    <div className="item-media-container">
      <span className="item-media-title">Media</span>
      <div className="item-media">
        {media.map((item, index) => (
          <img
            key={index}
            src={item}
            alt={item.alt || "Review media"}
            className="item-media-item"
          />
        ))}
      </div>
    </div>
  );
}

export default ItemPage;
