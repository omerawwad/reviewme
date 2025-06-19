import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import useSearch from "../hooks/useSearch";
import "../styles/SearchPage.css";
import PaginationControls from "../components/smallComponents/PaginationControls";
import SimplePagination from "../components/smallComponents/SimplePagination";
import ItemsSkeleton from "./stillPages/ItemsSkeleton";

const SearchPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");

  // Get query from URL parameters
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const query = params.get("q") || "";
    setSearchQuery(query);
  }, [location.search]);

  const { items, loading, error, pageInfo, setPage } = useSearch(
    searchQuery,
    currentPage,
    10
  );

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    setPage(newPage);
  };

  const handleItemClick = (itemId) => {
    navigate(`/item/${itemId}`);
  };

  if (loading && currentPage === 1) {
    return (
      <div className="search-page">
        <div className="search-container">
          {Array.from({ length: 5 }).map((_, index) => (
            <ItemsSkeleton key={index} />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="search-page">
        <div className="search-container">
          <h1>Search Results</h1>
          <div className="error">Error: {error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="search-page">
      <div className="search-container">
        <SearchPageHeader
          searchQuery={searchQuery}
          totalResults={pageInfo.total_items}
        />
        {pageInfo.total_items > 0 ? (
          <>
            <div className="search-results">
              {items.map((item) => (
                <ItemCard key={item.id} item={item} onClick={handleItemClick} />
              ))}
            </div>

            {/* Pagination */}
            <SimplePagination
              pageInfo={pageInfo}
              handlePageChange={handlePageChange}
            />
          </>
        ) : (
          <div className="no-results">
            {searchQuery ? (
              <p>No items found for "{searchQuery}"</p>
            ) : (
              <p>Enter a search query to find items</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

function SearchPageHeader({ searchQuery, totalResults = 0 }) {
  return (
    <div className="search-header">
      <span className="search-results-title">
        Search Results For
        {searchQuery && <span className="search-query"> "{searchQuery}"</span>}
      </span>
      <span className="results-count">
        {totalResults} item
        {totalResults !== 1 ? "s" : ""}
      </span>
    </div>
  );
}

function ItemCard({ item, onClick }) {
  return (
    <div className="search-item" onClick={() => onClick(item.id)}>
      <div className="item-header">
        <span className="item-name">{item.name}</span>
        <div className="item-rating">
          <span className="rating">★ {item.average_rating || 0}</span>
          <span className="review-count">
            ({item.review_count || 0} reviews)
          </span>
        </div>
      </div>
      <span className="item-description">{item.description}</span>
    </div>
  );
}

export default SearchPage;
