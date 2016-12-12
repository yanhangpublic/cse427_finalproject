
package org.apache.hadoop.finalproject;
import java.io.*;


import org.apache.hadoop.io.WritableComparable;

public class IntPairWritable implements WritableComparable<IntPairWritable> {

  Integer left;
  Integer right;

  /**
   * Empty constructor - required for serialization.
   */ 
  public IntPairWritable() {

  }

  /**
   * Constructor with two String objects provided as input.
   */ 
  public IntPairWritable(int left, int right) {
    this.left = left;
    this.right = right;    
  }

  /**
   * Serializes the fields of this object to out.
   */
  public void write(DataOutput out) throws IOException {
    
    /*
     * TODO implement
     */
   out.writeInt(left);
   out.writeInt(right);
  }

  /**
   * Deserializes the fields of this object from in.
   */
  public void readFields(DataInput in) throws IOException {
    
    /*
     * TODO implement
     */
	  left = in.readInt();
	  right = in.readInt();
  }

  /**
   * Compares this object to another StringPairWritable object by
   * comparing the left strings first. If the left strings are equal,
   * then the right strings are compared.
   */
  public int compareTo(IntPairWritable other) {
    int ret = 0;
    
    if (equals(other)){
    	ret = 0;
    }
    else{
    	int LeftResult = 0;
    	if(left<other.left)
    		LeftResult=-1;
    	else if(left==other.left)
    		LeftResult=0;
    	else if (left>other.left)
    		LeftResult=1;
    	
    	int RightResult = 0;
    	if(right<other.right)
    		RightResult=-1;
    	else if(right==other.right)
    		RightResult=0;
    	else if (right>other.right)
    		RightResult=1;
    	if (LeftResult > 0){
    		ret = 1;
    	}
    	if (LeftResult < 0){
    		ret = -1;
    	}
    	if (LeftResult == 0){
    		if (RightResult > 0){
        		ret = 1;
        	}
        	if (RightResult < 0){
        		ret = -1;
        	}
		if (RightResult == 0)
		    ret = 0;
    	}
//    	if (left > right){
//    		ret = 1;
//    	}
//    	if (LeftResult < 0){
//    		ret = -1;
//    	}
//    	if (LeftResult == 0){
//    		if (RightResult > 0){
//        		ret = 1;
//        	}
//        	if (RightResult < 0){
//        		ret = -1;
//        	}
//    	}
    }   
    return ret;
  }

  /**
   * A custom method that returns the two strings in the 
   * StringPairWritable object inside parentheses and separated by
   * a comma. For example: "(left,right)".
   */
  public String toString() {
     return "(" + left + "," + right + ")";
  }

  /**
   * The equals method compares two StringPairWritable objects for 
   * equality. The equals and hashCode methods have been automatically
   * generated by Eclipse by right-clicking on an empty line, selecting
   * Source, and then selecting the Generate hashCode() and equals()
   * option. 
   */
  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    IntPairWritable other = (IntPairWritable) obj;
    
    if((left==other.left)&&(right==(other.right)))
      return true;
    return false;
  }

  /**
   * The hashCode method generates a hash code for a StringPairWritable 
   * object. The equals and hashCode methods have been automatically
   * generated by Eclipse by right-clicking on an empty line, selecting
   * Source, and then selecting the Generate hashCode() and equals()
   * option. 
   */
  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((left == null) ? 0 : left.hashCode());
    result = prime * result + ((right == null) ? 0 : right.hashCode());
    return result;
  }
  public int getLeft()
  {
	  return left;
  }
  public int getRight()
  {
	  return right;
  }
}
