use rand::Rng;
use std::collections::HashMap;

/// A structure implementing a buffer of limited size `s`, which
/// keeps a random sample of distinct elements seen so far, each with
/// an associated random “score” u in [0,1).
///
/// We maintain a parameter `p` such that for any seen distinct element a,
/// Pr[a is in the buffer] = p.  (See the paper/Knuth’s note for invariants.) :contentReference[oaicite:2]{index=2}
pub struct CvmDistinctEstimator<T> {
    s: usize,                // capacity of the buffer
    buffer: HashMap<T, f64>, // map element -> its random u
    p: f64,                  // current inclusion threshold
}

impl<T> CvmDistinctEstimator<T>
where
    T: std::hash::Hash + Eq + Clone,
{
    /// Create a new estimator with buffer capacity `s` (>=1)
    pub fn new(s: usize) -> Self {
        assert!(s >= 1, "buffer size s must be >=1");
        Self {
            s,
            buffer: HashMap::new(),
            p: 1.0,
        }
    }

    /// Process a new stream element `a`.
    pub fn process(&mut self, a: T) {
        let mut rng = rand::rng();
        let u: f64 = rng.random(); // uniform in [0,1)

        if u < self.p {
            // Either new element, or we may replace one
            if self.buffer.contains_key(&a) {
                // Already present: update maybe its u to the new smaller u?
                let old = self.buffer.get(&a).unwrap();
                if u < *old {
                    self.buffer.insert(a.clone(), u);
                }
            } else {
                // Not present yet
                if self.buffer.len() < self.s {
                    self.buffer.insert(a.clone(), u);
                } else {
                    // Buffer full: find element with largest u
                    if let Some((max_elem, &max_u)) = self
                        .buffer
                        .iter()
                        .max_by(|&(_, &u1), &(_, &u2)| u1.partial_cmp(&u2).unwrap())
                    {
                        let max_elem = max_elem.clone();
                        if u < max_u {
                            // remove the one with max_u
                            let max_elem = max_elem.clone();
                            self.buffer.remove(&max_elem);
                            // insert the new element
                            self.buffer.insert(a.clone(), u);
                            // update p to be the new max_u
                            self.p = max_u;
                        }
                    }
                }
            }
        }
    }

    /// Return the current estimate of the number of distinct elements seen so far.
    ///
    /// Since Pr[element is in buffer] = p, we use `|buffer| / p` as the unbiased estimator.
    pub fn estimate(&self) -> f64 {
        (self.buffer.len() as f64) / self.p
    }
}

fn main() {
    let mut est = CvmDistinctEstimator::new(5); // buffer of size 100

    let stream = vec![1000, 1, 2, 3, 2, 1, 4, 5, 4, 6, 7, 8, 1, 9];
    for x in stream {
        est.process(x);
    }

    println!("Estimated distinct = {}", est.estimate());
}
