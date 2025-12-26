from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, Donation
from app.forms import DonationForm

donor_bp = Blueprint('donor', __name__)


@donor_bp.route('/')
@login_required
def dashboard():
    active_campaigns = Campaign.query.filter_by(is_active=True).order_by(Campaign.created_at.desc()).all()
    my_donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.created_at.desc()).limit(5).all()
    total_donated = db.session.query(db.func.sum(Donation.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    return render_template('donor/dashboard.html',
                          title='Dashboard Donor',
                          campaigns=active_campaigns,
                          my_donations=my_donations,
                          total_donated=total_donated)


@donor_bp.route('/donate/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def donate(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if not campaign.is_active:
        flash('Campaign ini sudah tidak aktif.', 'warning')
        return redirect(url_for('donor.dashboard'))
    
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            user_id=current_user.id,
            campaign_id=campaign.id,
            amount=form.amount.data,
            message=form.message.data
        )
        campaign.collected_amount += form.amount.data
        db.session.add(donation)
        db.session.commit()
        flash(f'Terima kasih! Donasi sebesar Rp {form.amount.data:,.0f} berhasil.', 'success')
        return redirect(url_for('donor.history'))
    
    return render_template('donor/donate.html', title=f'Donasi - {campaign.title}', form=form, campaign=campaign)


@donor_bp.route('/history')
@login_required
def history():
    donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.created_at.desc()).all()
    return render_template('donor/history.html', title='Riwayat Donasi', donations=donations)


@donor_bp.route('/donations/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_donation(id):
    donation = Donation.query.get_or_404(id)
    
    # Ensure user can only edit their own donations
    if donation.user_id != current_user.id:
        abort(403)
    
    form = DonationForm(obj=donation)
    old_amount = donation.amount
    
    if form.validate_on_submit():
        # Update campaign collected amount
        donation.campaign.collected_amount -= old_amount
        donation.campaign.collected_amount += form.amount.data
        
        donation.amount = form.amount.data
        donation.message = form.message.data
        db.session.commit()
        flash('Donasi berhasil diperbarui!', 'success')
        return redirect(url_for('donor.history'))
    
    return render_template('donor/edit_donation.html', title='Edit Donasi', form=form, donation=donation)


@donor_bp.route('/donations/<int:id>/delete', methods=['POST'])
@login_required
def delete_donation(id):
    donation = Donation.query.get_or_404(id)
    
    # Ensure user can only delete their own donations
    if donation.user_id != current_user.id:
        abort(403)
    
    # Update campaign collected amount
    donation.campaign.collected_amount -= donation.amount
    
    db.session.delete(donation)
    db.session.commit()
    flash('Donasi berhasil dihapus!', 'success')
    return redirect(url_for('donor.history'))
