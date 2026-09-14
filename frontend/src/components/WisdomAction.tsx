import React from 'react';
import { WisdomAction as WisdomActionType } from '../types';

interface Props {
  wisdomAction: WisdomActionType;
  onCreatePlan: () => void;
}

export const WisdomAction: React.FC<Props> = ({ wisdomAction, onCreatePlan }) => {
  return (
    <div className="wisdom-action-card">
      <div className="wisdom-action-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        Wisdom → Action
      </div>
      
      <div className="wisdom-step">
        <div className="wisdom-label">Evidence Suggests</div>
        <div className="wisdom-text">{wisdomAction.evidence_suggests}</div>
      </div>
      
      <div className="wisdom-step">
        <div className="wisdom-label">What It Means</div>
        <div className="wisdom-text">{wisdomAction.what_it_means}</div>
      </div>
      
      <div className="wisdom-step">
        <div className="wisdom-label">What To Do Next</div>
        <div className="wisdom-text">{wisdomAction.what_to_do_next}</div>
      </div>
      
      <div className="wisdom-footer">
        <button className="btn btn-secondary" onClick={onCreatePlan}>
          Create action plan →
        </button>
      </div>
    </div>
  );
};
